FORMAT = """title: {room_number}
description: Find room no. {number} in the White Void

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    "rm_u_0001",
    "rm_u_0002",
    "rm_u_0003",
    "rm_u_0004",
    "rm_u_0005",
    "rm_u_0006",
    "rm_u_0007",
    "rm_u_0008",
    "rm_u_0009",
    "rm_u_0010",
    "rm_u_0011",
    "rm_u_0012",
    "rm_u_0013",
    "rm_u_0014",
    "rm_u_0015",
    "rm_u_0016",
    "rm_u_0017",
    "rm_u_0018",
    "rm_u_0019",
    "rm_u_0020",
    "rm_u_0021",
    "rm_u_0022",
    "rm_u_0023",
    "rm_u_0024",
    "rm_u_0025",
    "rm_u_0026",
    "rm_u_0027",
    "rm_u_0028",
]



for index, room_name in enumerate(ROOM_NAMES):
    with open(f"achievements/room_w{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            number=index+1,
            room_number=f"W{str(index+1).rjust(2, '0')}",
            room_name=room_name
        ))