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

var patchesByFile = new Dictionary<string, List<(PatchData, Achievement)>>();
foreach (Achievement achievement in achievements) {
    foreach (PatchData patch in achievement.Patches) {
        if (!patchesByFile.ContainsKey(patch.FileName)) {
            patchesByFile.Add(patch.FileName, new List<(PatchData, Achievement)>());
        }
        patchesByFile[patch.FileName].Add((patch, achievement));
    }
}


{ // Initialize achievements data
    UndertaleCode code = Data.GameObjects.ByName("obj_inventory").EventHandlerFor(EventType.Create, (uint) 0, Data);
    var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
    var codeString = decompileContext.DecompileToString();
    codeString += "ds_achievements = ds_map_create();\n";
    codeString += "ds_ach_titles = ds_map_create();\n";
    codeString += "ds_ach_descs = ds_map_create();\n";
    foreach (var achievement in achievements) {
        codeString += $"ds_map_set(obj_inventory.ds_achievements, \"{achievement.Id}\", undefined);\n";
        codeString += $"ds_map_set(obj_inventory.ds_ach_titles, \"{achievement.Id}\", \"{achievement.Header.Title}\");\n";
        codeString += $"ds_map_set(obj_inventory.ds_ach_descs, \"{achievement.Id}\", \"{achievement.Header.Description}\");\n";
    }
    importGroup.QueueReplace(code, codeString);
}

{ // Load achievements data
    UndertaleGlobalInit scr_load_achievements = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_load_achievements"),
    };
    Data.GlobalInitScripts.Add(scr_load_achievements);
    importGroup.QueueReplace(scr_load_achievements.Code, @"function scr_load_achievements() {
        var filename = ""achievements.vs"";
        if (file_exists(filename)) {
            ini_open(filename);
            ds_map_read(obj_inventory.ds_achievements, ini_read_string(""Save"", ""data"", """"));
            ini_close();
        }
    }");

    
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
    importGroup.QueueReplace(scr_save_achievements.Code, @"function scr_save_achievements() {
        ini_open(""achievements.vs"");
        ini_write_string(""Save"", ""data"", ds_map_write(obj_inventory.ds_achievements));
        ini_close();
    }");

    UndertaleCode code = Data.Code.ByName("gml_GlobalScript_exit_game");
    var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
    List<string> codeString = decompileContext.DecompileToString().Split('\n').ToList();
    codeString.Insert(108, "scr_save_achievements();");
    importGroup.QueueReplace(code, string.Join('\n', codeString));
}

{ // Global function to call when you get an achievement
    UndertaleGlobalInit scr_get_achievement = new UndertaleGlobalInit() {
        Code = UndertaleCode.CreateEmptyEntry(Data, "gml_GlobalScript_scr_get_achievement"),
    };
    Data.GlobalInitScripts.Add(scr_get_achievement);
    importGroup.QueueReplace(scr_get_achievement.Code, @"function scr_get_achievement(achievement_id) {
        if ds_map_find_value(obj_inventory.ds_achievements, achievement_id) != undefined
            return;
        
        ds_map_replace(obj_inventory.ds_achievements, achievement_id, date_current_datetime());

        // TO DO: notification push
        with (obj_notification)
            y -= 16

        var notification = instance_create_layer(0, 0, ""Text"", obj_notification);
        notification.title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id)
    }");
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
    draw_sprite(spr_ex_medal, image_index, x + 224-10, y + 136);");
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
        dx = 0
        target_x = 0");
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
            
            if ds_map_find_value(obj_inventory.ds_achievements, achievement_id) != undefined
                txt_color = c_ltgray;
        }

        
        
        dx = lerp(dx, target_x, 0.3);");
        importGroup.QueueAppend(obj_achievement_item.EventHandlerFor(EventType.Draw, Data), 
        @"draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_left);
        var title = ds_map_find_value(obj_inventory.ds_ach_titles, achievement_id);

        if title != undefined
            draw_text_color(x + 24, y + 8, title, txt_color, txt_color, txt_color, txt_color, 1);
        
        if ds_map_find_value(obj_inventory.ds_achievements, achievement_id) != undefined
            if hovered
                draw_sprite(spr_ex_medal, image_index, x + 10, y + 9);
            else
                draw_sprite(spr_ex_medal_c, image_index, x + 10, y + 9);
        
        // draw_set_alpha(bg_alpha);
        // if dx >= 1
        //     draw_rectangle_color(x, y, x + dx, y + 16, bg_color, bg_color, bg_color, bg_color, false);
        // draw_set_alpha(1);");
    }

    {
        var obj_achievement_zoom = new UndertaleGameObject() {
            Name = Data.Strings.MakeString("obj_achievement_zoom"),
        };
        Data.GameObjects.Add(obj_achievement_zoom);
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Create, Data), 
        @"zoom_mode = false;
        achievement_id = """";
        image_speed = 0.2");
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Step, Data), 
        @"if scr_input_check_pressed(4)
            zoom_mode = !zoom_mode;");
        importGroup.QueueAppend(obj_achievement_zoom.EventHandlerFor(EventType.Draw, Data), 
        @"if zoom_mode {
            draw_rectangle_color(0, 24, 224 , 144 - 24, c_black, c_black, c_black, c_black, false);
            draw_rectangle_color(4, 24, 224 - 5, 144 - 24, c_gray, c_gray, c_gray, c_gray, true);

            var description = ds_map_find_value(obj_inventory.ds_ach_descs, achievement_id);
            if description != undefined {
                draw_set_font(fnt_past2);
                draw_set_valign(fa_center);
                draw_set_halign(fa_center);
                draw_text_ext_color(224 / 2, 144 / 2 - 8, description, 0, 200, c_ltgray, c_ltgray, c_ltgray, c_ltgray, 1);
            }

            var dt = ds_map_find_value(obj_inventory.ds_achievements, achievement_id);
            if dt != undefined {
                draw_set_font(fnt_past2);
                draw_set_valign(fa_center);
                draw_set_halign(fa_center);
                var datetime_str = string(""{0} {1}"", date_date_string(dt), date_time_string(dt));
                draw_text_ext_color(224 / 2, 144 - 36, datetime_str, 4, 200, c_gray, c_gray, c_gray, c_gray, 1);
                draw_sprite(spr_ex_medal, image_index, 224 / 2, 36);
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
        nb_pages = nb_achievements div items_per_page;
        achievement_items = [];
        for (var i = 0 ; i < items_per_page; i++) {
            array_push(achievement_items, instance_create_depth(12, 2 + i * 18 , depth - 1, obj_achievement_item));
        }
        instance_create_depth(0, 0, depth - 2, obj_achievement_zoom)
        array_sort(achievement_ids, true);
        nb_achievements_got = 0;
        achievement_dates = ds_map_values_to_array(obj_inventory.ds_achievements);
        for (var i = 0 ; i < array_length(achievement_dates); i++) {
            if achievement_dates[i] != undefined {
                nb_achievements_got++;
            }
        }
        ");
        importGroup.QueueAppend(obj_achievements_list.EventHandlerFor(EventType.Step, Data), 
        @"input_left_p = scr_input_check_pressed(0);
        input_right_p = scr_input_check_pressed(1);
        input_up_p = scr_input_check_pressed(2);
        input_down_p = scr_input_check_pressed(3);
        input_enter_p = scr_input_check_pressed(4);
        input_enter = scr_input_check(4);
        
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

        if !obj_achievement_zoom.zoom_mode {
            if selected_index < items_per_page {
                if input_right_p {
                    page += 1;
                    if audio_is_playing(snd_pageturn)
                        audio_stop_sound(snd_pageturn);
                    audio_play_sound(snd_pageturn, 1, false, 1, 0.5);
                } else if input_left_p {
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
            achievement_items[i].achievement_id = achievement_ids[i + page * items_per_page];
            achievement_items[i].hovered = selected_index == i;
            if (selected_index == i) {
                obj_achievement_zoom.achievement_id = achievement_ids[i + page * items_per_page];
            }
        }");
        importGroup.QueueAppend(obj_achievements_list.EventHandlerFor(EventType.Draw, Data), 
        @"draw_rectangle_color(0, 0, 224, 144, c_black, c_black, c_black, c_black, false);

        draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_center);
        draw_text_color(224 / 2, 144 - 28, string(""{0} of {1}"", page + 1, nb_pages), c_gray, c_gray, c_gray, c_gray, 1);
        
        draw_set_font(fnt_past2);
        draw_set_valign(fa_center);
        draw_set_halign(fa_right);
        draw_text_color(224 - 24, 144 - 12, string(""{0} / {1}"", nb_achievements_got, nb_achievements), c_gray, c_gray, c_gray, c_gray, 1);
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

    { // Add the achievement options in ds_menu_main
        UndertaleCode obj_menu_Create_0 = Data.GameObjects.ByName("obj_menu").EventHandlerFor(EventType.Create, (uint) 0, Data);
        var decompileContext = new DecompileContext(globalDecompileContext, obj_menu_Create_0, decompilerSettings);
        var codeLines = decompileContext.DecompileToString().Split('\n');
        codeLines[32] = "ds_menu_main = create_menu_page([scrScript(12), UnknownEnum.Value_0, \"resume_game\", 821], [scrScript(84), UnknownEnum.Value_1, UnknownEnum.Value_6, 2834], [scrScript(82), UnknownEnum.Value_7, UnknownEnum.Value_9, 417], [scrScript(13), UnknownEnum.Value_1, UnknownEnum.Value_1, 823], [scrScript(14), UnknownEnum.Value_0, \"end_game\", 1402], [\"ACHIEVEMENTS\", UnknownEnum.Value_10, UnknownEnum.Value_9, spr_placeholder]);";
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

{ // Apply achievements patches
    foreach (KeyValuePair<string, List<(PatchData, Achievement)>> entry in patchesByFile) {
        UndertaleCode code = Data.Code.ByName(entry.Key);
        var decompileContext = new DecompileContext(globalDecompileContext, code, decompilerSettings);
        List<string> codeLines = decompileContext.DecompileToString().Split('\n').ToList();

        entry.Value.Sort((a, b) => b.Item1.LineNumber - a.Item1.LineNumber);
        foreach (var (patch, achievement) in entry.Value) {
            codeLines.InsertRange(patch.LineNumber - 1, patch.String.Replace("{+achievement}", $"{{ scr_get_achievement(\"{achievement.Id}\"); }}").Split('\n'));
        }
        
        importGroup.QueueReplace(entry.Key, string.Join('\n', codeLines));
    }
}


importGroup.Import();


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