FORMAT = """title: {title}
description: Get hit a total of {number} times

// PATCH gml_Object_obj_player_Step_0 1833
if obj_inventory.hit_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    75, 100, 150, 200, 250, 500
]

TITLES = {
    1: "Ouch!",
    500: "Masochist",
}

for number in NUMBERS:
    with open(f"achievements/hit_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Ouch! ({number}/{max(NUMBERS)})")
        ))
