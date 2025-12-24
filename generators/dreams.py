FORMAT_GRAY = """title: The {ordinal} dream
description: Start watching Gray's {ordinal} dream

// PATCH gml_Room_{room_name}_Create 1
if !instance_exists(obj_rest)
{{+achievement}}
"""

FORMAT_LILLIE = """title: The {ordinal} dream (Hard)
description: Start watching Lillie's {ordinal} dream

// PATCH gml_Room_{room_name}_Create 1
if !instance_exists(obj_rest)
{{+achievement}}
"""


FORMAT_CIF = """title: My little lightbringer
description: Start watching Cif's dream

// PATCH gml_Room_rm_cdream_001_Create 1
if !instance_exists(obj_rest)
{{+achievement}}
"""

FORMAT_VOID = """title: Do you remember why you're here?
description: Start watching Gray's final dream while being VOIDed

// PATCH gml_Room_rm_dreamIX_void_Create 1
if !instance_exists(obj_rest)
{{+achievement}}
"""

GRAY_DREAMS = [
    "rm_dreamI_001",
    "rm_dreamII_001",
    "rm_dreamIII_001",
    "rm_dreamIV_001",
    "rm_dreamV_001",
    "rm_dreamVI_001",
    "rm_dreamVII_001",
    "rm_dreamVIII_001",
    "rm_dreamIX_001",
]

LILLIE_DREAMS = [
    "rm_ldream0_001",
    "rm_ldreamI_001",
    "rm_ldreamII_001",
    "rm_ldreamIII_001",
    "rm_ldreamIV_001",
    "rm_ldreamV_001",
    "rm_ldreamVI_001",
    "rm_ldreamVII_001",
    "rm_ldreamIX_001",
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
    9: "final",
}


for index, room_name in enumerate(GRAY_DREAMS):
    with open(f"achievements/dream_gray_{index+1}", "w") as f:
        f.write(FORMAT_GRAY.format(ordinal=ORDINALS[index+1], room_name=room_name))

for index, room_name in enumerate(LILLIE_DREAMS):
    with open(f"achievements/dream_lillie_{index+1}", "w") as f:
        f.write(FORMAT_LILLIE.format(ordinal=ORDINALS[index+1], room_name=room_name))

with open(f"achievements/dream_cif", "w") as f:
        f.write(FORMAT_CIF)

with open(f"achievements/dream_gray_voided", "w") as f:
        f.write(FORMAT_VOID)