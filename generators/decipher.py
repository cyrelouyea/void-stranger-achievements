FORMAT = """title: {title}
description: Use the Void Memory a total of {number} times

// PATCH gml_Object_obj_player_Step_0 1220
if obj_inventory.memory_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_mural_Step_0 658
if obj_inventory.memory_counter >= {number}
    {{+achievement}}"""

NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    100, 200, 300, 400, 500
]

TITLES = {
    1: "Don't ask how I know",
    500: "Extinct language expert",
}

for number in NUMBERS:
    with open(f"achievements/void_memory_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Don't ask how I know ({number}/{max(NUMBERS)})")
        ))
