FORMAT = """title: {title}
description: {description}

// PATCH gml_Object_obj_player_Step_0 1935
if obj_inventory.medal_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_player_add_Step_0 556
if obj_inventory.medal_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    1, 50, 100, 500, 1000,
    2000, 3000, 4000, 5000,
    7_500, 10_000
]

TITLES = {
    1: "Medal",
    10_000: "HOARDER",
}

DESCRIPTIONS = {
    1: "Collect a medal in 0stRanger or Cif's Challenge"
}

for number in NUMBERS:
    with open(f"achievements/medal_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Medal ({number}/{max(NUMBERS)})"),
            description=DESCRIPTIONS.get(number, f"Collect a total of {number} medals in 0stRanger or Cif's Challenge")
        ))