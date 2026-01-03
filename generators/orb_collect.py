FORMAT = """title: {title}
description: Absorb a total of {number} orbs in Stage 0

// PATCH gml_Object_obj_ex_powerup_Step_0 247
if obj_inventory.orb_collect_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50,
    100, 200, 300, 400, 500,
]

TITLES = {
    500: "Orb devourer",
}

for number in NUMBERS:
    with open(f"achievements/stage_0_orb_collect_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Orb collector ({number}/{max(NUMBERS)})")
        ))
