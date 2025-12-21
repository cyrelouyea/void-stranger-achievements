FORMAT = """title: {title}
description: Play for {time_text}

// PATCH gml_Object_obj_inventory_Step_0 44
if ds_list_find_value(ds_rcrds, 12) >= {hours} && ds_list_find_value(ds_rcrds, 11) >= {minutes} && ds_list_find_value(ds_rcrds, 11) >= {seconds}
    {{+achievement}}
"""

THRESHOLDS = [
    (0, 1, 0, "1 minute", "Void stranger"),
    (0, 5, 0, "5 minutes", "Void foreigner"),
    (0, 10, 0, "10 minutes", "Void outsider"),
    (0, 30, 0, "30 minutes", "Void newcomer"),
    (1, 0, 0, "1 hour", "Void tourist"),
    (2, 0, 0, "2 hours", "Void visitor"),
    (5, 0, 0, "5 hours", "Void traveler"),
    (10, 0, 0, "10 hours", "Void explorer"),
    (20, 0, 0, "20 hours", "Void commoner"),
    (30, 0, 0, "30 hours", "Void occupant"),
    (40, 0, 0, "40 hours", "Void civilian"),
    (50, 0, 0, "50 hours", "Void citizen"),
    (100, 0, 0, "100 hours", "Void dweller"),
]

for index, (hours, minutes, seconds, time_text, title) in enumerate(THRESHOLDS):
    with open(f"achievements/time_{index+1}", "w") as f:
        f.write(FORMAT.format(
            title=title,
            time_text=time_text,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ))
