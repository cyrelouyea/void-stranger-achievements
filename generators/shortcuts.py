FORMAT = """title: {ordinal} shortcut
description: Access the {ordinal} shortcut

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""

ORDINALS = {
    0: "1st",
    1: "2nd",
    2: "3rd",
    3: "4th",
    4: "5th",
}

with open("generators/shortcuts.txt", "r") as f:
    shortcuts = f.read().splitlines()


for index, shortcut in enumerate(shortcuts):
    room_data = shortcut.split()
    room_name = room_data[0]

    with open(f"achievements/room_shortcut_{index+1}", "w") as f:
        f.write(FORMAT.format(ordinal=ORDINALS[index], room_name=room_name))