FORMAT = """title: {lord_name}'s chamber
description: Find {lord_name}'s chamber

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""

with open("generators/chambers.txt", "r") as f:
    chambers = f.read().splitlines()

for index, shortcut in enumerate(chambers):
    room_data = shortcut.split()
    room_name = room_data[0]
    lord_name = room_data[1]

    with open(f"achievements/room_chamber_{lord_name.lower()}", "w") as f:
        f.write(FORMAT.format(lord_name=lord_name, room_name=room_name))