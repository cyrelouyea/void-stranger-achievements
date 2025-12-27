FORMAT = """title: {room_number}
description: Go to {room_number}

// PATCH gml_Room_{room_name}_Create 1
if ds_grid_get(obj_inventory.ds_player_info, 22, 1) != 1000
    {{+achievement}}
"""


with open("generators/room_numbers_ex.txt", "r") as f:
    text = f.read()



for line in text.splitlines():
    room_data = line.split()

    room_number = room_data[0].rjust(3, "0")
    room_name = room_data[1]


    with open(f"achievements/room_e{room_number.replace('?', 'x').lower()}", "w") as f:
        f.write(FORMAT.format(room_number=f"E{room_number.replace('_', ' ')}", room_name=room_name))