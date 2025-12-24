FORMAT = """title: {title}
description: Fall a total of {number} times

// PATCH gml_Object_obj_player_Step_0 1826
if ds_list_find_value(obj_inventory.ds_rcrds, 6) >= {number}
    {{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50,
    75, 100, 150, 200, 250
]

TITLES = {
    250: "Thrill seeker"
}

for number in NUMBERS:
    with open(f"achievements/fall_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"AaaaaaAAAA- ({number}/{max(NUMBERS)})")
        ))
