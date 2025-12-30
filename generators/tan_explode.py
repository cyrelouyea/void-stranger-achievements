FORMAT = """title: {title}
description: Make a one-eyed statue self-explode a total of {number} times

// PATCH gml_Object_obj_boulder_Step_0 640
if obj_inventory.tan_explode_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500
]

TITLES = {
    "Appeasement": 500
}

for number in NUMBERS:
    with open(f"achievements/tan_explode_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Make them go away... ({number}/{max(NUMBERS)})")
        ))
