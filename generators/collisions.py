FORMAT = """title: {title}
description: {description}

// PATCH gml_Object_obj_enemy_cs_Step_0 54
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_cg_Step_0 60
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_ct_Step_0 82
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_cm_Step_0 124
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_cl_Step_0 44
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_cc_Step_0 44
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_co_Step_0 56
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_enemy_ch_Step_0 50
if !place_meeting(x, y, obj_boulder)  && obj_inventory.collision_counter >= {number}
{{+achievement}}"""


NUMBERS = [
    1, 5, 10, 20, 30, 40, 50, 75, 
    100, 150, 200, 250
]

TITLES = {
    1: "Road accident",
    250: "Collision expert"
}

DESCRIPTIONS = {
    1: "Make two or more enemies collide"
}

for number in NUMBERS:
    with open(f"achievements/collision_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Road accident ({number}/{max(NUMBERS)})"),
            description=DESCRIPTIONS.get(number, f"Make two or more enemies collide a total of {number} times")
        ))
