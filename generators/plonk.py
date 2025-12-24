FORMAT = """title: {title}
description: Plonk a total of {number} entit{plural}

// PATCH gml_Object_obj_player_Step_0 866
if obj_inventory.plonk_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 100
]

TITLES = {
    100: "Serial plonker"
}

for number in NUMBERS:
    with open(f"achievements/plonk_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number, 
            plural="ies" if number > 1 else "y", 
            title=TITLES.get(number, f"Plonk! ({number}/{max(NUMBERS)})")
        ))
