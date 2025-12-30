FORMAT = """title: {title}
description: Use the void rod {number} times

// PATCH gml_Object_obj_player_Step_0 1145
if obj_inventory.void_rod_counter >= {number}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 826
if obj_inventory.void_rod_counter >= {number}
    {{+achievement}}
"""

NUMBERS_LIMIT = [
    5, 10, 25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 
    1_000, 2_000, 3_000, 4_000, 5_000,
    6_000, 7_000, 8_000, 9_000, 10_000
]

TITLES = {
    10_000: "Void Architect"
}

for number in NUMBERS_LIMIT:
    with open(f"achievements/void_rod_{str(number).rjust(len(str(max(NUMBERS_LIMIT))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"{number} tiles moved!")
        ))
