FORMAT = """title: {title}
description: {description}

""" 

PATCH_FORMAT = """// PATCH gml_Object_{obj}_Step_0 {ln}
if obj_inventory.{name}_kill_counter >= {number}
{{+achievement}}
"""

ENEMIES = (
    ("leech", "obj_enemy_cl", (166, 181, ), ),
    ("maggot", "obj_enemy_cc", (148, 163, ), ),
    ("smile", "obj_enemy_cs", (184, 192, ), ),
    ("beaver", "obj_enemy_cg", (282, 291, ), ),
    ("eye", "obj_enemy_ch", (85, 124, ), ),
    ("octahedron", "obj_enemy_co", (154, 169, ), ),
    ("mimic", "obj_enemy_cm", (283, 322, ), ),
    ("spider", "obj_enemy_ct", (147, 152, ), ),
    ("fly", "obj_enemy_cf", (166, )),
)

DEFAULT_NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    75, 100, 150, 200, 250,
]

FLY_NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    60, 70, 80, 90, 100
]

SPIDER_NUMBERS = [1]

for name, obj, linenumbers in ENEMIES:
    numbers = DEFAULT_NUMBERS

    if name == "fly":
        numbers = FLY_NUMBERS
    elif name == "spider":
        numbers = SPIDER_NUMBERS

    for number in numbers:
        with open(f"achievements/enemy_{name}_kill_{str(number).rjust(len(str(max(numbers))), '0')}", "w") as f:
            title = f"{name.capitalize()} killer" + ((f" ({number}/{max(numbers)})") if number > 1 else "")
            if number == max(numbers):
                title = f"{name.capitalize()} hater"

            text = FORMAT.format(
                title=title,
                description=f"Kill a {name}" + (f" a total of {number} times" if number > 1 else "")
            )

            for ln in linenumbers:
                text += PATCH_FORMAT.format(obj=obj, ln=ln, name=name, number=number)
            
            f.write(text)