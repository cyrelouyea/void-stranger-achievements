FORMAT_NORMAL = """title: {room_number}
description: Go to {room_number} as Gray or Cif

// PATCH gml_Room_{room_name}_Create 1
if (global.loop == 0)
    {{+achievement}}
"""

FORMAT_HARD = """title: {room_number} (Hard)
description: Go to {room_number} as Lillie

// PATCH gml_Room_{room_name}_Create 1
if (global.loop == 1)
    {{+achievement}}
"""


with open("generators/room_numbers.txt", "r") as f:
    text = f.read()



for line in text.splitlines():
    room_data = line.split()

    room_number = room_data[0].rjust(3, "0")
    room_number_int = int(room_number[:3])
    room_name = room_data[1]

    loop = None
    if len(room_data) > 2:
        loop = int(room_data[2])
    
    if loop is None or loop == 0:
        with open(f"achievements/room_b{room_number}", "w") as f:
            f.write(FORMAT_NORMAL.format(room_number=f"B{room_number}", room_name=room_name))

    if loop is None or loop == 1:
        with open(f"achievements/room_b{room_number}_hard", "w") as f:
            f.write(FORMAT_HARD.format(room_number=f"B{room_number}", room_name=room_name))