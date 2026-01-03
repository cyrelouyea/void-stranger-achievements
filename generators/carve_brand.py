FORMAT = """title: {lord} brand
description: Carve {lord} brand in one of the brand rooms

// PATCH gml_Object_obj_secret_exit_Step_0 {ln}
{{+achievement}}
"""

LORDS = [
    ("Add's", 52),
    ("Eus's", 56),
    ("Bee's", 60),
    ("Mon's", 64),
    ("Tan's", 68),
    ("Gor's", 72),
    ("Lev's", 76),
    ("Cif's", 80),
    ("Empty", 84),
    ("Player's", 112),
    ("Lily's", 92),
    ("Trailer", 88),
]

for lord, ln in LORDS:
    with open(f"achievements/carve_brand_{lord.replace("'", "_").lower()}", "w") as f:
        f.write(FORMAT.format(lord=lord, ln=ln))



