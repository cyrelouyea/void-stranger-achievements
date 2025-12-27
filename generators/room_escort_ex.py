FORMAT = """title: {room_number}
description: Go to egg escort room no. 1  

// PATCH gml_Room_{room_name}_Create 1
if ds_grid_get(obj_inventory.ds_player_info, 22, 1) != 1000
    {{+achievement}}
"""


ROOM_NAMES = [
    "rm_test2_065",
    "rm_test2_066",
    "rm_test2_067",
    "rm_test2_068",
    "rm_test2_069",
    "rm_test2_070",
    "rm_test2_071",
    "rm_test2_072",
    "rm_test2_073",
]

for index, room_name in enumerate(ROOM_NAMES):
    with open(f"achievements/room_eg{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(room_number=f"EG{str(index+1).rjust(2, '0')}", room_name=room_name))