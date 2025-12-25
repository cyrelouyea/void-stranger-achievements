FORMAT = """title: {title}
description: Activate Lev's statues a total of {number} times

// PATCH gml_Object_obj_player_Alarm_8 16
if obj_inventory.pissed_lev_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_player_Alarm_8 32
if obj_inventory.pissed_lev_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_player_Other_17 16
if obj_inventory.pissed_lev_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_boulder_Alarm_7 7
if obj_inventory.pissed_lev_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 
    100, 250, 500
]

TITLES = {
}

for number in NUMBERS:
    with open(f"achievements/pissed_lev_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"One wrong move... ({number}/{max(NUMBERS)})")
        ))
