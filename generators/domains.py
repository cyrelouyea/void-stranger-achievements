FORMAT = """title: The {ordinal} domain
description: Reach a room in the {ordinal} domain
"""

PATCH_FORMAT = """// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""

DOMAINS = [
    (1, 28), 
    (29, 56), 
    (57, 84), 
    (85, 112), 
    (113, 140), 
    (141, 168),
    (169, 196), 
    (197, 224), 
    (225, 254),
]

ORDINALS = {
    0: "first",
    1: "second",
    2: "third",
    3: "fourth",
    4: "fifth",
    5: "sixth",
    6: "seventh",
    7: "eighth",
    8: "ninth",
}

with open("generators/room_numbers.txt", "r") as f:
    text = f.read()


domain_to_room_names = [set() for i in range(9)]


for line in text.splitlines():
    room_data = line.split()

    room_number = room_data[0].rjust(3, "0")
    room_number_int = int(room_number[:3])
    room_name = room_data[1]

    domain_number = next((i for i, (b, t) in enumerate(DOMAINS) if b <= room_number_int <= t), None)

    if domain_number is not None:
        domain_to_room_names[domain_number].add(room_name)


for i, room_names in enumerate(domain_to_room_names):
    s = FORMAT.format(ordinal=ORDINALS[i])

    for room_name in room_names:
        s += PATCH_FORMAT.format(room_name=room_name)
    
    with open(f"achievements/domain_{i+1}", "w") as f:
        f.write(s)