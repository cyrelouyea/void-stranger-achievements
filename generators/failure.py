FORMAT_MEET = """title: The {ordinal} failure
description: Find the failure in the {ordinal} domain

// PATCH gml_Object_{obj}_Create_0 1
if scr_f_check() != 0 && !global.failure
{{+achievement}}"""

FORMAT_TALK = """title: {title}
description: Talk to the failure in the {ordinal} domain

// PATCH gml_Object_{obj}_Alarm_0 1
if (ds_grid_get(obj_inventory.ds_equipment, 0, 0) == 1 && global.memory_toggle == true)
{{+achievement}}"""


FAILURES = [
    "obj_npc_failure_001",
    "obj_npc_failure_002",
    "obj_npc_failure_003",
    "obj_npc_failure_004",
    "obj_npc_failure_005",
    "obj_npc_failure_006",
    "obj_npc_failure_007",
    "obj_npc_failure_008",
]

TITLES = [
    "UNDYING FLESH",
    "CURSE THAT WORM",
    "A SIMPLE BEING",
    "THE MOST REPUGNANT OF ALL",
    "A GENTLE BEING",
    "SLUGGISH AND INDECISIVE",
    "A HEARTLESS BEING",
    "A FRAGILE BEING"
]

ORDINALS = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
}


for index, obj_name in enumerate(FAILURES):
    with open(f"achievements/npc_failure_{index+1}", "w") as f:
        f.write(FORMAT_MEET.format(ordinal=ORDINALS[index+1], obj=obj_name))

    with open(f"achievements/npc_failure_talk_{index+1}", "w") as f:
        f.write(FORMAT_TALK.format(title=TITLES[index], ordinal=ORDINALS[index+1], obj=obj_name))