FORMAT = """title: The {ordinal} memory
description: Recall the {ordinal} memory

// PATCH gml_Object_obj_memories_album_Step_0 411
if ds_grid_get(obj_inventory.ds_album, {pic_number}, 0)
    {{+achievement}}
"""

PIC_NUMBERS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

ORDINALS = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
    9: "ninth",
    10: "last",
}


for pic_number in PIC_NUMBERS:
    with open(f"achievements/memory_{pic_number}", "w") as f:
        f.write(FORMAT.format(
            pic_number=pic_number,
            ordinal=ORDINALS[pic_number]
        ))
