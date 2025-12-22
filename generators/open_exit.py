FORMAT = """title: {title}
description: Open a total of {number} exit using switch tiles

// PATCH gml_Object_obj_exit_Step_0 9
if obj_inventory.open_exit_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500,
    1_000,
]

TITLES = {
    1_000: "Locksmith"
}

for number in NUMBERS:
    with open(f"achievements/tiles_open_exit_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Unlocked ({number}/{max(NUMBERS)})")
        ))
