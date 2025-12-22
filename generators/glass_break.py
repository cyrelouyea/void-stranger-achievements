FORMAT = """title: {title}
description: Break a total of {number} glass tiles

// PATCH gml_Object_obj_glassfloor_Step_0 97
if obj_inventory.glass_break_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500,
    1_000,
]

TITLES = {
    1_000: "Ice breaker"
}

for number in NUMBERS:
    with open(f"achievements/tiles_glass_break_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"*Kssshhhk* ({number}/{max(NUMBERS)})")
        ))
