FORMAT = """title: {title}
description: Learn more about Lord {lord} with the lonely ones

// PATCH gml_Object_obj_player_Step_0 1232
if special_message == {message}
{{+achievement}}"""


EGGS = [
    (8, "The Beginning (1)", "Add"),
    (9, "The Beginning (2)", "Add"),
    (10, "The Beginning (3)", "Add"),
    (11, "The Beginning (4)", "Add"),
    (12, "The Beginning (5)", "Add"),
    (13, "The Beginning (6)", "Add"),

    (14, "The First Traitor (1)", "Eus"),
    (15, "The First Traitor (2)", "Eus"),
    (16, "The First Traitor (3)", "Eus"),
    (17, "The First Traitor (4)", "Eus"),

    (18, "The Craving (1)", "Bee"),
    (19, "The Craving (2)", "Bee"),
    (20, "The Craving (3)", "Bee"),
    (21, "The Craving (4)", "Bee"),
    (22, "The Craving (5)", "Bee"),

    (23, "The Second Traitor (1)", "Mon"),
    (24, "The Second Traitor (2)", "Mon"),
    (25, "The Second Traitor (3)", "Mon"),
    (26, "The Second Traitor (4)", "Mon"),

    (27, "The Raging (1)", "Tan"),
    (28, "The Raging (2)", "Tan"),
    (29, "The Raging (3)", "Tan"),
    (30, "The Raging (4)", "Tan"),

    (31, "The Third Traitor (1)", "Gor"),
    (32, "The Third Traitor (2)", "Gor"),
    (33, "The Third Traitor (3)", "Gor"),

    (35, "The Devious (1)", "Lev"),
    (36, "The Devious (2)", "Lev"),
    (37, "The Devious (3)", "Lev"),
    (38, "The Devious (4)", "Lev"),
]

for index, (message, title, lord) in enumerate(EGGS):
    with open(f"achievements/npc_egg_lord_{str(index).rjust(len(str(len(EGGS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            message=message,
            title=title,
            lord=lord
        ))