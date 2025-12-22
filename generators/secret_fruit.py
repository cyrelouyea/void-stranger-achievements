FORMAT = """title: Secret {fruit}
description: Find the secret {fruit}

// PATCH gml_Object_obj_ee_bonus_Step_0 11
if ee_id == {ee_id}
    {{+achievement}}
"""

FRUIT_NAMES = [
    "Succubus",
    "Daikon",
    "Banana",
    "Vanilla",
    "Onion",
    "Orange",
    "Avocado",
]


for number, fruit in enumerate(FRUIT_NAMES):
    with open(f"achievements/secret_fruit_{fruit.lower()}", "w") as f:
        f.write(FORMAT.format(
            ee_id=number,
            fruit=fruit
        ))
