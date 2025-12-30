FORMAT = """title: Secret Code #{number}
description: Use the secret code #{number} in the music room

// PATCH gml_Object_obj_soundtest_Step_0 54
if i == {index}
{{+achievement}}
"""

CODES = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
]

for code in CODES:
    with open(f"achievements/music_art_{str(code).rjust(len(str(len(CODES))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=code+1,
            index=code,
        ))
