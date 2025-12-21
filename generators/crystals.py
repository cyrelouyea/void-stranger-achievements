FORMAT = """title: {title}
description: Collect {number} memory crystal{plural}

// PATCH gml_GlobalScript_scr_savetoken 24
if ds_list_find_value(obj_inventory.ds_rcrds, 13) >= {number}
    {{+achievement}}
"""

CRYSTALS_LIMIT = [
    1, 2, 4, 8, 16, 32, 64, 128
]

TITLES = {
    1: "First crystal!",
    128: "Crystal clear"
}

for nb_crystals in CRYSTALS_LIMIT:
    with open(f"achievements/memory_crystals_{nb_crystals}", "w") as f:
        f.write(FORMAT.format(
            number=nb_crystals, 
            plural="s" if nb_crystals > 1 else "", 
            title=TITLES.get(nb_crystals, f"{nb_crystals} crystals!")
        ))
