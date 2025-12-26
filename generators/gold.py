FORMAT = """title: {title}
description: Turn to gold a total of {number} times

// PATCH gml_Object_obj_player_golden_Create_0 2
if obj_inventory.gold_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 75, 100
]

TITLES = {
    100: "Midas Touch"
}

for number in NUMBERS:
    with open(f"achievements/golden_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Golden ({number}/{max(NUMBERS)})")
        ))
