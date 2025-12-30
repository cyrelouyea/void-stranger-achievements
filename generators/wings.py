FORMAT = """title: {title}
description: Use the wings a total of {number} times

// PATCH gml_Object_obj_player_Step_0 652
if obj_inventory.wings_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 2354
if obj_inventory.wings_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    100, 250, 500, 1000
]

TITLES = {
    1: "Just leap and believe!",
    1000: "Angelic",
}

for number in NUMBERS:
    with open(f"achievements/wings_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Just leap and believe! ({number}/{max(NUMBERS)})")
        ))
