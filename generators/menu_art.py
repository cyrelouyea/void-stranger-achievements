FORMAT = """title: Menu Art ({name})
description: Look at the {name} menu art

// PATCH gml_Object_obj_menu_Step_0 21
if ds_grid_get(ds_, 3, menu_option[page]) == {image}
    {{+achievement}}"""

MENU_ART = [
    ("spr_menu_continue", "Gray"),
    ("spr_menu_continue_2", "Lillie"),
    ("spr_menu_continue_friend", "Ninnie"),
    ("spr_menu_continue_mercenary", "Mercenary"),
    ("spr_menu_continue_mirror2", "Mimic Lillie"),
    ("spr_menu_continue_friend_b", "Ninnie and Lillie"),
    ("spr_menu_continue_3", "Cif"),
    ("spr_menu_continue_bride", "Bride"),
    ("spr_menu_continue_child", "Lost Child"),
    ("spr_menu_continue_oldman", "Old Man"),
    ("spr_menu_continue_friend_c", "Lillie and Ninnie"),
    ("spr_menu_continue_nun", "Nun"),
    ("spr_menu_continue_ykko", "Sister"),
    ("spr_menu_continue_nomad", "Treasure Hunter"),
    ("spr_menu_continue_mirror", "Mimic Gray"),
    ("spr_menu_continue_lily", "Lily"),
    ("spr_menu_continue_nollatytto", "???"),
    ("spr_menu_continue_nolla", "Dev"),
]


for index, (image, name) in enumerate(MENU_ART):
    with open(f"achievements/menu_art_{str(index+1).rjust(len(str(len(MENU_ART))), '0')}", "w") as f:
        f.write(FORMAT.format(
            name=name,
            image=image,
        ))

