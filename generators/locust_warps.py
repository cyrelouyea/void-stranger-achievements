FORMAT = """title: {title}
description: Skip a total of {number} rooms with locust warps

// PATCH gml_GlobalScript_scr_roomselect 51
if obj_inventory.locust_warp_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    25, 50, 100, 200, 300, 400,
    500, 750, 1000
]

TITLES = {
    1000: "Puzzle hater"
}


for number in NUMBERS:
    with open(f"achievements/locust_warp_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Puzzle hater ({number}/{max(NUMBERS)})")
        ))

