using System.Linq;
using Underanalyzer.Decompiler;
using UndertaleModLib.Compiler;

public class HeaderData {
    public string Title { get; set; }
    public string Description { get; set; }
}

public class PatchData {
    public int LineNumber { get; set; }
    public string FileName { get; set; }
    public string String { get; set; }
}

public class Achievement {
    public string Id { get; set; }
    public HeaderData Header { get; set; }
    public PatchData[] Patches { get; set; }
}

public class Counter {
    public string Id { get; set; }
    public PatchData[] Patches { get; set; }
}

EnsureDataLoaded();

GlobalDecompileContext globalDecompileContext = new(Data);
IDecompileSettings decompilerSettings = new DecompileSettings() {
    OpenBlockBraceOnSameLine = false,
    RemoveSingleLineBlockBraces = true,
    EmptyLineAfterBlockLocals = true,
    EmptyLineAroundEnums = true,
    EmptyLineAroundBranchStatements = true,
    EmptyLineBeforeSwitchCases = true,
    EmptyLineAfterSwitchCases= false,
    EmptyLineAroundFunctionDeclarations = true,
    EmptyLineAroundStaticInitialization = true,
};
CodeImportGroup importGroup = new(Data, globalDecompileContext, decompilerSettings);

// Load achievements data
string runningDirectory = Path.GetDirectoryName(ScriptPath);
string achievementsPath = Path.GetFullPath(Path.Combine(runningDirectory, "achievements"));
string[] achievementsFiles = Directory.GetFiles(achievementsPath);
Achievement[] achievements = achievementsFiles.Select(parseAchievementFile).ToArray();

var patchesByFile = new Dictionary<string, List<PatchData>>();
foreach (Achievement achievement in achievements) {
    foreach (PatchData patch in achievement.Patches) {
        if (!patchesByFile.ContainsKey(patch.FileName)) {
            patchesByFile.Add(patch.FileName, new List<PatchData>());
        }

        var newString = Regex
            .Replace(patch.String, @"\{\+achievement(:(?<time>\d+))?\}",
                m => {
                    var time = m.Groups["time"].Value;
                    if (time != "") {
                        return $"{{ scr_get_achievement(\"{achievement.Id}\", {time}); }}";
                    } else {
                        return $"{{ scr_get_achievement(\"{achievement.Id}\"); }}";
                    }
                }
            );

        patchesByFile[patch.FileName].Add(new PatchData() {
            LineNumber = patch.LineNumber,
            FileName = patch.FileName,
            String = newString
                .Replace("{-achievement}", $"{{ scr_remove_achievement(\"{achievement.Id}\"); }}"), 
        });
    }
}

// Load custom counters data
string countersPath = Path.GetFullPath(Path.Combine(runningDirectory, "counters"));
string[] countersFiles = Directory.GetFiles(countersPath);
Counter[] counters = countersFiles.Select(parseCounterFile).ToArray();

List<string> records_init = new List<string>();
List<string> records_save_list = new List<string>();
List<string> records_load_list = new List<string>();

foreach (Counter counter in counters) {
    foreach (PatchData patch in counter.Patches) {
        if (!patchesByFile.ContainsKey(patch.FileName)) {
            patchesByFile.Add(patch.FileName, new List<PatchData>());
        }
        patchesByFile[patch.FileName].Add(new PatchData() {
            LineNumber = patch.LineNumber,
            FileName = patch.FileName,
            String = patch.String.Replace("{{counter}}", $"obj_inventory.{counter.Id}_counter"), 
        });
    }
    records_init.Add($"{counter.Id}_counter = 0;");
    records_save_list.Add($"ini_write_real(\"Counters\", \"{counter.Id}\", obj_inventory.{counter.Id}_counter);");
    records_load_list.Add($"obj_inventory.{counter.Id}_counter = ini_read_real(\"Counters\", \"{counter.Id}\", 0);");
}


{ // Initialize achievements data
    UndertaleCode code = Data.GameObjects.ByName("obj_inventory").EventHandlerFor(EventType.Create, (uint) 0, Data);
    var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
    var codeString = decompileContext.DecompileToString();
    codeString += "achievements_loaded = false;\n";
    codeString += "nb_achievements_got = 0\n";
    codeString += "ds_achievements = ds_map_create();\n";
    codeString += "ds_ach_titles = ds_map_create();\n";
    codeString += "ds_ach_descs = ds_map_create();\n";
    codeString += "ds_ach_revealed = ds_map_create();\n";
    foreach (var achievement in achievements) {
        codeString += $"ds_map_set(obj_inventory.ds_achievements, \"{achievement.Id}\", undefined);\n";
        codeString += $"ds_map_set(obj_inventory.ds_ach_titles, \"{achievement.Id}\", \"{achievement.Header.Title}\");\n";
        codeString += $"ds_map_set(obj_inventory.ds_ach_descs, \"{achievement.Id}\", \"{achievement.Header.Description}\");\n";
        codeString += $"ds_map_set(obj_inventory.ds_ach_revealed, \"{achievement.Id}\", false);\n";
    }
    codeString += string.Join('\n', records_init);
    importGroup.QueueReplace(code, codeString);
}


{ // Load achievements data
    UndertaleGlobalInit scr_load_achievements = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_load_achievements"),
    };
    Data.GlobalInitScripts.Add(scr_load_achievements);

    var codeStr = @"function scr_load_achievements() {
        var filename = ""achievements.vs"";
        if (file_exists(filename)) {
            var _tmp_ds_achievement = ds_map_create();
            ini_open(filename);
            ds_map_read(_tmp_ds_achievement, ini_read_string(""Save"", ""data"", """"));
            {{records_load_str}}
            ini_close();

            var keys = ds_map_keys_to_array(_tmp_ds_achievement);
            for (var i = 0; i < array_length(keys) ; i++) {
                if ds_map_exists(obj_inventory.ds_achievements, keys[i]) {
                    ds_map_replace(obj_inventory.ds_achievements, keys[i], ds_map_find_value(_tmp_ds_achievement, keys[i]));
                }
            }
        }

        achievement_dates = ds_map_values_to_array(obj_inventory.ds_achievements);
        for (var i = 0 ; i < array_length(achievement_dates); i++) {
            if !is_undefined(achievement_dates[i]) {
                obj_inventory.nb_achievements_got++;
            }
        }

        obj_inventory.achievements_loaded = true;
        scr_achievement_menueyecatch();
    }";
    codeStr = codeStr.Replace("{{records_load_str}}", string.Join('\n', records_load_list));
    importGroup.QueueReplace(scr_load_achievements.Code, codeStr);

    
    UndertaleCode code = Data.GameObjects.ByName("obj_init").EventHandlerFor(EventType.Create, (uint) 0, Data);
    var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
    string codeString = decompileContext.DecompileToString();
    codeString += "scr_load_achievements();\n";
    importGroup.QueueReplace(code, codeString);
}

{ // Save achievements data
    UndertaleGlobalInit scr_save_achievements = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_save_achievements"),
    };
    Data.GlobalInitScripts.Add(scr_save_achievements);

    var codeStr = @"function scr_save_achievements() {
        ini_open(""achievements.vs"");
        ini_write_string(""Save"", ""data"", ds_map_write(obj_inventory.ds_achievements));
        {{records_save_str}}
        ini_close();
    }";
    codeStr = codeStr.Replace("{{records_save_str}}", string.Join('\n', records_save_list));
    importGroup.QueueReplace(scr_save_achievements.Code, codeStr);

    {  // save achievements when exiting the game
        UndertaleCode code = Data.Code.ByName("gml_GlobalScript_exit_game");
        var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
        List<string> codeString = decompileContext.DecompileToString().Split('\n').ToList();
        codeString.Insert(108, "scr_save_achievements();");
        importGroup.QueueReplace(code, string.Join('\n', codeString));
    }

    {  // also save achievements every time the game is saved (in case of crash) 
        UndertaleCode code = Data.Code.ByName("gml_GlobalScript_scr_savegame");
        var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
        List<string> codeString = decompileContext.DecompileToString().Split('\n').ToList();
        codeString.Insert(157, "scr_save_achievements();");
        importGroup.QueueReplace(code, string.Join('\n', codeString));
    }
}

{ // Global function to call when you get an achievement
    UndertaleGlobalInit scr_get_achievement = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_get_achievement"),
    };
    Data.GlobalInitScripts.Add(scr_get_achievement);
    importGroup.QueueReplace(scr_get_achievement.Code, @"function scr_get_achievement(achievement_id, delay = 0) {
        if delay == 0 {
            if !instance_exists(obj_inventory) || !obj_inventory.achievements_loaded {
                return;
            }

            if !is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
                return;
            
            ds_map_replace(obj_inventory.ds_achievements, achievement_id, date_current_datetime());
            obj_inventory.nb_achievements_got++;
            scr_achievement_menueyecatch();

            with (obj_notification)
                y -= 16;

            var notification = instance_create_depth(0, 0, -300, obj_notification);
            notification.title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id);
        } else {
            var notification = instance_create_depth(0, 0, -300, obj_notification_delay);
            notification.achievement_id = achievement_id;
            notification.alarm[0] = delay;
        }
    }");
}

{ // Global function to call when you remove an achievement
    UndertaleGlobalInit scr_remove_achievement = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_remove_achievement"),
    };
    Data.GlobalInitScripts.Add(scr_remove_achievement);
    importGroup.QueueReplace(scr_remove_achievement.Code, @"function scr_remove_achievement(achievement_id) {
        if is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
            return;
        
        ds_map_replace(obj_inventory.ds_achievements, achievement_id, undefined);
        obj_inventory.nb_achievements_got--;
        scr_achievement_menueyecatch();
    }");
}

{ // Global function to update the pause menu art
    UndertaleGlobalInit scr_achievement_menueyecatch = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_achievement_menueyecatch"),
    };
    Data.GlobalInitScripts.Add(scr_achievement_menueyecatch);
    importGroup.QueueReplace(scr_achievement_menueyecatch.Code, @"function scr_achievement_menueyecatch() {
        with (obj_inventory) {
            var perc = nb_achievements_got / ds_map_size(ds_achievements);

            var thresholds = [
                0.04,
                0.08,
                0.12,
                0.16,
                0.20,
                0.24,
                0.28,
                0.32,
                0.36,
                0.40,
                0.44,
                0.5,
            ]

            var sprites = [
                spr_menu_achievements_a,
                spr_menu_achievements_b,
                spr_menu_achievements_c,
                spr_menu_achievements_d,
                spr_menu_achievements_e,
                spr_menu_achievements_f,
                spr_menu_achievements_g,
                spr_menu_achievements_h,
                spr_menu_achievements_i,
                spr_menu_achievements_j,
                spr_menu_achievements_k,
                spr_menu_achievements_l,
                spr_menu_achievements_m,
            ]

            for (var i = 0; i < array_length(thresholds); i++) {
                if perc < thresholds[i] {
                    with (obj_menu) {
                        ds_grid_set(obj_menu.ds_menu_main, 3, 4, sprites[i]);
                        return;
                    }
                }
            }

            ds_grid_set(obj_menu.ds_menu_main, 3, 4, sprites[array_length(sprites) - 1]);
        }
    }");
}

{ // Object to delay notification
    var obj_notification_delay = new UndertaleGameObject() {
        Name = Data.Strings.MakeString("obj_notification_delay"),
        Persistent = true
    };
    Data.GameObjects.Add(obj_notification_delay);
    importGroup.QueueAppend(obj_notification_delay.EventHandlerFor(EventType.Create, Data), 
    @"achievement_id = """";");
    importGroup.QueueAppend(obj_notification_delay.EventHandlerFor(EventType.Alarm, (uint) 0, Data), 
    @"if !instance_exists(obj_inventory) || !obj_inventory.achievements_loaded {
        return;
    }
    
    if !is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
        return;
    
    ds_map_replace(obj_inventory.ds_achievements, achievement_id, date_current_datetime());
    obj_inventory.nb_achievements_got++;
    scr_achievement_menueyecatch();
    
    with (obj_notification)
        y -= 16;

    var notification = instance_create_depth(0, 0, -300, obj_notification);
    notification.title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id);
    instance_destroy();");
}

{ // Achievement notification object
    var obj_notification = new UndertaleGameObject() {
        Name = Data.Strings.MakeString("obj_notification"),
        Persistent = true
    };
    Data.GameObjects.Add(obj_notification);

    importGroup.QueueAppend(obj_notification.EventHandlerFor(EventType.Create, Data), 
    @"title = ""...""
    x = -224
    target_x = 0
    image_speed = 0.3
    alarm[0] = 120
    if (audio_is_playing(snd_ex_jingle))
        audio_stop_sound(snd_ex_jingle);
    var isfx = audio_play_sound(snd_ex_jingle, 1, false);
    audio_sound_pitch(isfx, 1.1);");
    importGroup.QueueAppend(obj_notification.EventHandlerFor(EventType.Alarm, (uint) 0, Data), "target_x = 224; alarm[1] = 32");
    importGroup.QueueAppend(obj_notification.EventHandlerFor(EventType.Alarm, (uint) 1, Data), "instance_destroy();");
    importGroup.QueueAppend(obj_notification.EventHandlerFor(EventType.Step, Data), "x = lerp(x, target_x, 0.2)");
    importGroup.QueueAppend(obj_notification.EventHandlerFor(EventType.Draw, Data), 
    @"draw_rectangle_color(x + 0, y + 128, x + 224, y + 144, c_black, c_black, c_black, c_black, false);
    draw_set_font(fnt_past2);
    draw_set_valign(fa_center);
    draw_set_halign(fa_center);
    draw_text_color(x + 112, y + 136, title, c_white, c_white, c_white, c_white, 1);
    draw_sprite(spr_ex_medal, image_index, x + 10, y + 136);
    draw_sprite(spr_ex_medal, image_index, x + 224-10, y + 136);
    draw_set_valign(fa_top);
    draw_set_halign(fa_left);");
}



{ // Achievements menu

    { // obj_achievement_item
        var obj_achievement_item = new UndertaleGameObject() {
            Name = Data.Strings.MakeString("obj_achievement_item"),
        };
        Data.GameObjects.Add(obj_achievement_item);
        importGroup.QueueAppend(obj_achievement_item.EventHandlerFor(EventType.Create, Data), 
        @"achievement_id = """"
        hovered = false;
        bg_color = c_white;
        bg_alpha = 0.5;
        txt_color = c_gray;
        target_x = 0;
        revealed = false;
        reveal_counter = 0;");
        importGroup.QueueAppend(obj_achievement_item.EventHandlerFor(EventType.Step, Data), 
        @"if hovered {
            image_speed = 0.2;
            target_x = 200;
            txt_color = c_white;
        } else {
            image_speed = 0;
            image_index = 0;
            target_x = 0;
            txt_color = c_gray;
            
            if !is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
                txt_color = c_ltgray;
        }
        ");
        importGroup.QueueAppend(obj_achievement_item.EventHandlerFor(EventType.Draw, Data), 
        @"draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_left);
        var title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id);

        if hovered && reveal_counter > 0 {
            draw_rectangle_color(
                224 / 2 - (reveal_counter / 60) * 224 / 2, y, 
                224 / 2 + (reveal_counter / 60) * 224 / 2 , y + 16, 
                c_gray, c_gray, c_gray, c_gray, false);
        }

        if !is_undefined(title) {
            var dx = 24;
            if hovered && obj_achievements_list.hold_reveal_counter > 0 {
                draw_set_halign(fa_center);
                title = ""HOLD TO REVEAL"";
                dx = 224 / 2 - 8
            }
            else if !revealed
                title = ""???""

            draw_text_color(x + dx, y + 8, title, txt_color, txt_color, txt_color, txt_color, 1);
        }
        
        if !is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
            if hovered
                draw_sprite(spr_ex_medal, image_index, x + 10, y + 9);
            else
                draw_sprite(spr_ex_medal_c, image_index, x + 10, y + 9);
                
        ");
    }

    {
        var obj_achievement_zoom = new UndertaleGameObject() {
            Name = Data.Strings.MakeString("obj_achievement_zoom"),
        };
        Data.GameObjects.Add(obj_achievement_zoom);
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Create, Data), 
        @"zoom_mode = false;
        achievement_id = """";
        image_speed = 0.2;
        revealed = false;");
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Step, Data), 
        @"if scr_input_check_pressed(4) {
            if revealed {
                zoom_mode = !zoom_mode;
            } else {

            }
        }");
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Draw, Data), 
        @"if zoom_mode {
            draw_rectangle_color(0, 24, 224 , 144 - 24, c_black, c_black, c_black, c_black, false);
            draw_rectangle_color(4, 24, 224 - 5, 144 - 24, c_gray, c_gray, c_gray, c_gray, true);

            var title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id);
            if !is_undefined(title) {
                draw_set_font(fnt_past2);
                draw_set_valign(fa_center);
                draw_set_halign(fa_center);
                draw_text_ext_color(224 / 2, 30, title, 8, 200, c_white, c_white, c_white, c_white, 1);
            }

            var description = ds_map_find_value(obj_inventory.ds_ach_descs, achievement_id);
            if !is_undefined(description) {
                draw_set_font(fnt_past2);
                draw_set_valign(fa_center);
                draw_set_halign(fa_center);
                draw_text_ext_color(224 / 2, 144 / 2, description, 10, 200, c_ltgray, c_ltgray, c_ltgray, c_ltgray, 1);
            }

            var dt = ds_map_find_value(obj_inventory.ds_achievements, achievement_id);
            if !is_undefined(dt) {
                draw_set_font(fnt_past2);
                draw_set_valign(fa_center);
                draw_set_halign(fa_center);
                var datetime_str = string(""{0} {1}"", date_date_string(dt), date_time_string(dt));
                draw_text_ext_color(224 / 2, 144 - 36, datetime_str, 4, 200, c_gray, c_gray, c_gray, c_gray, 1);
                draw_sprite(spr_ex_medal, image_index, 16, 36);
                draw_sprite(spr_ex_medal, image_index, 224 - 16, 36);
            }
        }");

    }

    { // obj_achievements_list
        var obj_achievements_list = new UndertaleGameObject() {
            Name = Data.Strings.MakeString("obj_achievements_list"),
        };
        Data.GameObjects.Add(obj_achievements_list);
        importGroup.QueueAppend(obj_achievements_list.EventHandlerFor(EventType.Create, Data), 
        @"with (obj_pause)
            absolute_pause_check = true;
        page = 0;
        selected_index = 0;
        items_per_page = 6;
        image_speed = 0.1;
        achievement_ids = ds_map_keys_to_array(obj_inventory.ds_achievements);
        nb_achievements = array_length(achievement_ids);
        nb_pages = ceil(nb_achievements / items_per_page);
        hold_reveal_counter = 0;
        achievement_items = [];
        for (var i = 0 ; i < items_per_page; i++) {
            array_push(achievement_items, instance_create_depth(12, 2 + i * 18 , depth - 1, obj_achievement_item));
        }
        instance_create_depth(0, 0, depth - 2, obj_achievement_zoom);
        ordered_by_date = false
        array_sort(achievement_ids, true);
        input_hold_time = 0
        first_input_enter = scr_input_check(4)");
        importGroup.QueueAppend(obj_achievements_list.EventHandlerFor(EventType.Step, Data), 
        @"input_left = scr_input_check(0);
        input_left_p = scr_input_check_pressed(0);
        input_right = scr_input_check(1);
        input_right_p = scr_input_check_pressed(1);
        input_up_p = scr_input_check_pressed(2);
        input_down_p = scr_input_check_pressed(3);
        input_enter_p = scr_input_check_pressed(4);
        input_enter = scr_input_check(4);
        input_pause_p = scr_input_check_pressed(5);

        if first_input_enter && !input_enter {
            first_input_enter = false
        }
        
        if input_enter_p {
            if selected_index == items_per_page {
                with (obj_pause)
                    absolute_pause_check = false;
                
                with (obj_achievement_item)
                    instance_destroy()

                with(obj_achievement_zoom)
                    instance_destroy()
                
                instance_destroy()

                return;
            }
        }

        if input_enter && !first_input_enter {
            if selected_index < items_per_page 
            && !achievement_items[selected_index].revealed {
                hold_reveal_counter++;

                if hold_reveal_counter > 60 {
                    hold_reveal_counter = 0
                    ds_map_replace(obj_inventory.ds_ach_revealed, achievement_items[selected_index].achievement_id, true);
                    audio_play_sound(snd_reveal, 1, false);
                }
            }
        } else {
            hold_reveal_counter = 0;
            
            if !obj_achievement_zoom.zoom_mode {
                if input_pause_p {
                    ordered_by_date = !ordered_by_date
                    if ordered_by_date {
                        array_sort(achievement_ids, function (current, next) {
                            var date1 = ds_map_find_value(obj_inventory.ds_achievements, next);
                            var date2 = ds_map_find_value(obj_inventory.ds_achievements, current);
                            if is_undefined(date1) {
                                date1 = date_create_datetime(1971, 1, 1, 0, 0, 0);
                            }
                            if is_undefined(date2) {
                                date2 = date_create_datetime(1971, 1, 1, 0, 0, 0)
                            }
                            return date_compare_datetime(date1, date2); 
                        });
                    } else {
                        array_sort(achievement_ids, true);
                    }
                }

                if selected_index < items_per_page {
                    if input_right || input_left {
                        input_hold_time++;
                    } else {
                        input_hold_time = 0;
                    }

                    if input_right_p || (input_right && input_hold_time > 20 && input_hold_time % 3 == 0) {
                        page += 1;
                        if audio_is_playing(snd_pageturn)
                            audio_stop_sound(snd_pageturn);
                        audio_play_sound(snd_pageturn, 1, false, 1, 0.5);
                    } else if input_left_p || (input_left && input_hold_time > 20 && input_hold_time % 3 == 0) {
                        page -= 1;
                        if audio_is_playing(snd_pageturn)
                            audio_stop_sound(snd_pageturn);
                        audio_play_sound(snd_pageturn, 1, false, 1, 0.5);
                    }
                }
                
                if input_down_p {
                    selected_index += 1;
                    audio_play_sound(snd_menu_1, 1, false);
                } else if input_up_p {
                    selected_index -= 1;
                    audio_play_sound(snd_menu_1, 1, false);
                }        
            }
        }

        if page < 0 {
            page += nb_pages;
        }

        if page >= nb_pages {
            page -= nb_pages;
        }
        

        if selected_index < 0 {
            selected_index += items_per_page + 1
        }

        if selected_index >= items_per_page + 1 {
            selected_index -= items_per_page + 1
        }

        for (var i = 0 ; i < items_per_page; i++) {
            var achievement_id = """"
            if (i + page * items_per_page < array_length(achievement_ids)) {
                achievement_id = achievement_ids[i + page * items_per_page];
            }

            achievement_items[i].achievement_id = achievement_id;
            achievement_items[i].hovered = selected_index == i;
            achievement_items[i].revealed = (
                !is_undefined(ds_map_find_value(obj_inventory.ds_achievements, achievement_id))
                || ds_map_find_value(obj_inventory.ds_ach_revealed, achievement_id)
            );
            achievement_items[i].reveal_counter = hold_reveal_counter;
            if (selected_index == i) {
                obj_achievement_zoom.achievement_id = achievement_id;
                obj_achievement_zoom.revealed = achievement_items[i].revealed;
            }
        }
        
        ");
        importGroup.QueueAppend(obj_achievements_list.EventHandlerFor(EventType.Draw, Data), 
        @"draw_rectangle_color(0, 0, 224, 144, c_black, c_black, c_black, c_black, false);

        draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_center);
        draw_text_color(224 / 2, 144 - 28, string(""{0} of {1}"", page + 1, nb_pages), c_gray, c_gray, c_gray, c_gray, 1);
        
        draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_right);
        draw_text_color(224 - 24, 144 - 12, string(""{0} / {1}"", obj_inventory.nb_achievements_got, nb_achievements), c_gray, c_gray, c_gray, c_gray, 1);
        draw_sprite(spr_ex_medal_c, image_index, 224 - 12, 144 - 11);
        
        var back_color = c_gray
        if selected_index == items_per_page
            back_color = c_white
        draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_center);
        draw_text_color(24, 144 - 12, ""< BACK"", back_color, back_color, back_color, back_color, 1);");
    }

    { // Patch create_menu_page to allow 6 options in a menu (default is 5)
        var key = "gml_GlobalScript_create_menu_page";
        UndertaleCode create_menu_page = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, create_menu_page, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n');
        codeLines[11] = "var ds_grid_id = ds_grid_create(6, argument_count);";
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }

    { // Patch language_menu to insert the achievements option
        var key = "gml_GlobalScript_language_menu";
        UndertaleCode language_menu = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, language_menu, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n');
        codeLines[6] = "ds_grid_set(obj_menu.ds_menu_main, 0, 4, \"ACHIEVEMENTS\"); ds_grid_set(obj_menu.ds_menu_main, 0, 5, scrScript(14));";
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }


    { // Add the achievement options in ds_menu_main
        UndertaleCode obj_menu_Create_0 = Data.GameObjects.ByName("obj_menu").EventHandlerFor(EventType.Create, (uint) 0, Data);
        var decompileContext = new DecompileContext(globalDecompileContext, obj_menu_Create_0, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n');
        codeLines[32] = "ds_menu_main = create_menu_page([scrScript(12), UnknownEnum.Value_0, \"resume_game\", 821], [scrScript(84), UnknownEnum.Value_1, UnknownEnum.Value_6, 2834], [scrScript(82), UnknownEnum.Value_7, UnknownEnum.Value_9, 417], [scrScript(13), UnknownEnum.Value_1, UnknownEnum.Value_1, 823], [\"ACHIEVEMENTS\", UnknownEnum.Value_10, UnknownEnum.Value_9, spr_menu_achievements_a], [scrScript(14), UnknownEnum.Value_0, \"end_game\", 1402]);";
        codeLines[153] = "Value_9, Value_10";
        importGroup.QueueReplace(obj_menu_Create_0, string.Join('\n', codeLines));
    }

    { // Invoke the obj_achievements_list in obj_menu
        UndertaleCode obj_menu_Step_0 = Data.GameObjects.ByName("obj_menu").EventHandlerFor(EventType.Step, (uint) 0, Data);
        var decompileContext = new DecompileContext(globalDecompileContext, obj_menu_Step_0, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n').ToList();
        codeLines[526] = "Value_8, Value_9, Value_10";
        codeLines[6] = "if (transition != true && draw_memories == false && !instance_exists(obj_achievements_list))";
        codeLines.Insert(280, 
        @"case UnknownEnum.Value_10:
            if (!instance_exists(obj_achievements_list))
            {
                audio_play_sound(snd_menu_3, 1, false);
                instance_create_depth(x, y, depth - 1, obj_achievements_list);
            }
            input_enter_p = 0;
            break;");
        importGroup.QueueReplace(obj_menu_Step_0, string.Join('\n', codeLines));
    }
}

{ // White Void also resets achievements 
    var key = "gml_Object_obj_npc_dr_ab___on_Other_12";
    UndertaleCode obj_npc_dr_ab___on_Other_12 = Data.Code.ByName(key);
    var decompileContext = new DecompileContext(globalDecompileContext, obj_npc_dr_ab___on_Other_12, decompilerSettings);
    var codeLines = decompileContext.DecompileToString().Split('\n');
    codeLines[13] = "obj_inventory.ds_achievements = ds_map_create();";
    importGroup.QueueReplace(key, string.Join('\n', codeLines));
}

{
    {
        var key = "gml_Object_obj_secret_exit_Create_0";
        UndertaleCode obj = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n').ToList();
        codeLines.Insert(146, @"str_answer_m = ""1111111111111111110001111111111101010111111111010001111111110101011111111100010111111111111000111111111111111111""
        for (var a = 0; a < 112; a += 1)
        {
            str_value = string_char_at(str_answer_m, 1 + a);
            var str_real = real(str_value);
            answer_array_m[a] = str_real;
        }");
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }

    {
        var key = "gml_Object_obj_secret_exit_Step_0";
        UndertaleCode obj = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n');
        codeLines[26] = "if (array_equals(current_array, answer_array_001) || array_equals(current_array, answer_array_002) || array_equals(current_array, answer_array_003) || array_equals(current_array, answer_array_004) || array_equals(current_array, answer_array_005) || array_equals(current_array, answer_array_006) || array_equals(current_array, answer_array_007) || array_equals(current_array, answer_array_008) || array_equals(current_array, answer_array_009) || array_equals(current_array, answer_array_010) || array_equals(current_array, answer_array_011) || array_equals(current_array, answer_array_999) || array_equals(current_array, answer_array_m) || end_secret == 1)";
        codeLines[109] = "else if array_equals(current_array, answer_array_999)";
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }

    {
        var key = "gml_Object_obj_secret_exit_Alarm_5";
        UndertaleCode obj = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n').ToList();
        codeLines.Insert(105, @"else if array_equals(current_array, answer_array_m) {
            with (obj_darkness) {
                instance_destroy()
            }
            room_instance_clear(room)
            instance_create_layer(0, 0, ""Effects2"", obj_miku_cif);
        }");
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }

    {
        var key = "gml_Object_obj_puumerkki_Other_11";
        UndertaleCode obj = Data.Code.ByName(key);
        var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n').ToList();
        codeLines.Insert(578, @"else if (brand_string == ""1111111111111111110001111111111101010111111111010001111111110101011111111100010111111111111000111111111111111111"")
        {
            str_script = 7108;
            ready_state = 2;
            confirm_state = 0;
        }");
        importGroup.QueueReplace(key, string.Join('\n', codeLines));
    }
}

{ // Achievement notification object
    var obj_miku_cif = new UndertaleGameObject() {
        Name = Data.Strings.MakeString("obj_miku_cif"),
        Persistent = true
    };
    Data.GameObjects.Add(obj_miku_cif);

    importGroup.QueueAppend(obj_miku_cif.EventHandlerFor(EventType.Create, Data), @"
    alarm[0] = 1000;
    alarm[1] = 1120;
    audio_group_stop_all(1);
    audio_group_stop_all(2);
    scr_audio_group_set_gain_vs(1, 0, 0);
    scr_audio_group_set_gain_vs(2, 0, 0);
    counter = 0;
    image_speed = 0.01;
    a1 = 0
    px = 112 - 8;
    py = 74 - 8;
    py2 = 0;
    py3 = 0;
    py4 = 0;
    py5 = 0;
    py6 = 0;");
    importGroup.QueueAppend(obj_miku_cif.EventHandlerFor(EventType.Alarm, (uint) 0, Data), @"instance_create_depth(0, 0, depth-1, obj_darkwall);");
    importGroup.QueueAppend(obj_miku_cif.EventHandlerFor(EventType.Alarm, (uint) 1, Data), @"game_end()");
    importGroup.QueueAppend(obj_miku_cif.EventHandlerFor(EventType.Draw, Data), 
    @"draw_rectangle_color(0, 0, 226, 146, c_black, c_black, c_black, c_black, false);

    draw_set_alpha(a1);
    if counter < 360 {
        draw_sprite(spr_miku_sleep, image_index, px, py);
    }
    draw_set_alpha(1);
    
    if counter > 390 && counter < 450 {
        draw_sprite(spr_miku_wakey, image_index, px, py);
    }
    
    if counter > 480 && counter <= 520 {
        draw_sprite(spr_miku_down, image_index, px, py);
    }
    if counter > 520 && counter <= 536 {
        draw_sprite(spr_miku_left, image_index, px, py);
    }
    if counter > 536 && counter <= 552 {
        draw_sprite(spr_miku_right, image_index, px, py);
    }
    if counter > 552 && counter <= 580 {
        draw_sprite(spr_miku_right, image_index, px, py);
    }
    if counter > 580 && counter <= 640 {
        draw_sprite(spr_miku_down, image_index, px, py);
    }
    if counter > 640 && counter <= 860 {
        draw_sprite(spr_miku_up, image_index, px, py);
    }

    if counter > 860 {
        draw_sprite(spr_miku_cif, 0, 0, 144 - py2)
        draw_sprite(spr_miku_cif, 1, 0, 144 - py3)
        draw_sprite(spr_miku_cif, 2, 0, 144 - py4)
        draw_sprite(spr_miku_cif, 3, 0, 144 - py5)
        draw_sprite(spr_miku_cif, 4, 0, 144 - py6)
    }
    
    ");
    importGroup.QueueAppend(obj_miku_cif.EventHandlerFor(EventType.Step, (uint) 0, Data), 
    @"
    if counter < 240 {
        a1 += 1.0 / 240.0;
    } else {
        a1 = 1
    }

    if counter > 700 && counter < 860 {
        py += 0.5
    }

    if counter > 860 {
        py2 = lerp(py2, 144, 0.1);
        py3 = lerp(py3, 144, 0.05);
        py4 = lerp(py4, 144, 0.07);
        py5 = lerp(py5, 144, 0.05);
        py6 = lerp(py6, 144, 0.06);
    }
    counter += 1;");
}

// { // Change the save file location
//     {
//         var key = "gml_GlobalScript_any_save_file_exists";
//         UndertaleCode obj = Data.Code.ByName(key);
//         var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
//         var codeLines = decompileContext.DecompileToString();
//         codeLines.Replace("\"save.vs\", "\"save_ach.vs\"")
//         codeLines.Replace("\"save_backup_1.vs\", "\"save_backup_1_ach.vs\"")
//         codeLines.Replace("\"save_backup_2.vs\", "\"save_backup_2_ach.vs\"")
//         importGroup.QueueReplace(key, codeLines);
//     }

//     {
//         var key = "gml_GlobalScript_scr_savegame";
//         UndertaleCode obj = Data.Code.ByName(key);
//         var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
//         var codeLines = decompileContext.DecompileToString();
//         codeLines.Replace("\"save.vs\", "\"save_ach.vs\"")
//         codeLines.Replace("\"save_backup_1.vs\", "\"save_backup_1_ach.vs\"")
//         codeLines.Replace("\"save_backup_2.vs\", "\"save_backup_2_ach.vs\"")
//         importGroup.QueueReplace(key, codeLines);
//     }

//     {
//         var key = "gml_Object_obj_npc_dr_ab___on_Other_12";
//         UndertaleCode obj = Data.Code.ByName(key);
//         var decompileContext = new DecompileContext(globalDecompileContext, obj, decompilerSettings);
//         var codeLines = decompileContext.DecompileToString();
//         codeLines.Replace("\"save.vs\", "\"save_ach.vs\"")
//         codeLines.Replace("\"save_backup_1.vs\", "\"save_backup_1_ach.vs\"")
//         codeLines.Replace("\"save_backup_2.vs\", "\"save_backup_2_ach.vs\"")
//         importGroup.QueueReplace(key, codeLines);
//     }
// }

importGroup.Import();

{ // Apply achievements and counters patches
    foreach (KeyValuePair<string, List<PatchData>> entry in patchesByFile) {
        UndertaleCode code = Data.Code.ByName(entry.Key);
        var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
        List<string> codeLines = decompileContext.DecompileToString().Split('\n').ToList();

        entry.Value.Sort((a, b) => b.LineNumber - a.LineNumber);
        foreach (var patch in entry.Value) {
            codeLines.InsertRange(patch.LineNumber - 1, patch.String.Split('\n'));
        }
        
        importGroup.QueueReplace(entry.Key, string.Join('\n', codeLines));
    }
}


importGroup.Import();


Counter parseCounterFile(string counterFile) {
    string text = File.ReadAllText(counterFile);
	string targetPattern = @"// PATCH ([^\n\r]+)";
	string[] sections = Regex.Split(text, targetPattern);

    return new Counter() {
        Id = Path.GetFileNameWithoutExtension(counterFile),
        Patches = parsePatches(sections),
    };
}

Achievement parseAchievementFile(string achievementFile) {
    string text = File.ReadAllText(achievementFile);
	string targetPattern = @"// PATCH ([^\n\r]+)";
	string[] sections = Regex.Split(text, targetPattern);

    return new Achievement() {
        Id = Path.GetFileNameWithoutExtension(achievementFile),
        Header = parseHeader(sections[0].Trim()),
        Patches = parsePatches(sections)
    };
}

PatchData[] parsePatches(string[] sections) {
    List<PatchData> patches = new List<PatchData>();

    for (int i = 1 ; i < sections.Length ; i += 2) {
        string[] patchHeader = Regex.Split(sections[i], @"\s+");

        patches.Add(new PatchData() {
            FileName = patchHeader[0],
            LineNumber = int.Parse(patchHeader[1]),
            String = sections[i + 1].Trim(),
        });
    }

    return patches.ToArray();
}

HeaderData parseHeader(string header) {
    Dictionary<string, string> map = new Dictionary<string, string>();
    
    foreach (string section in Regex.Split(header, @"[\n\r]+")) {
        string[] keyAndValue = Regex.Split(section, @":\s+");
        map[keyAndValue[0]] = keyAndValue[1];
    }

    return new HeaderData {
        Title = map["title"],
        Description = map["description"]
    };
}