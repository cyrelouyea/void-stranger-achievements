FORMAT = """title: {title}
description: Destroy with projectiles a total of {number} orbs in Stage 0

// PATCH gml_Object_obj_ex_powerup_Step_0 52
if obj_inventory.orb_shatter_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50,
    60, 70, 80, 90, 100
]

TITLES = {
    250: "Orb wrecker",
}

for number in NUMBERS:
    with open(f"achievements/stage_0_orb_shatter_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Orb shatterer ({number}/{max(NUMBERS)})")
        ))
