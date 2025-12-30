FORMAT = """title: {title}
description: Find a total of {number} locust idols

// PATCH gml_Object_obj_chest_small_Alarm_0 26
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_chest_small_Alarm_0 79
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_locust_collect_Step_0 12
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_locust_collect_Step_0 17
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_locust_collect_Step_0 22
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_chest_small_Alarm_0 111
if obj_inventory.locust_collect_counter >= {number}
{{+achievement}}"""

NUMBERS = [
    5, 10, 20, 30, 40, 50,
    100, 250, 500, 1000
]

TITLES = {
    "Locust gourmet": 1000
}

for number in NUMBERS:
    with open(f"achievements/locust_collect_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Yummy! ({number}/{max(NUMBERS)})")
        ))
