FORMAT = """title: {title}
description: Make a certain statue immovable a total of {number} times

// PATCH gml_Object_obj_boulder_Step_0 409
if obj_inventory.immovable_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_boulder_Step_0 213
if obj_inventory.immovable_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 
    75, 100, 150
]

TITLES = {
    "Cemented": 150
}

for number in NUMBERS:
    with open(f"achievements/immovable_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Immovable ({number}/{max(NUMBERS)})")
        ))
