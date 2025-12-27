FORMAT = """title: {line}
description: Fight against Cif's true form

// PATCH gml_Object_obj_cif_message_Step_0 11
if cm_n == {number} {{
    {{-achievement}}
    {{+achievement}}
}}
"""

LINES = [
    "Add...",
    "Long time ago...",
    "You created me and my sisters.",
    "Nurtured us.",
    "Guided us.",
    "You made us immovable.",
    "Everlasting.",
    "So that we'd be able to continue your work...",
    "Manusya.",
    "Their minds are so frail.",
    "So volatile.",
    "So misguided.",
    "So easily frustrated.",
    "They're lost.",
    "And even then...",
    "Their dreams are filled with stars.",
    "Time and time again...",
    "They reach for them, fruitlessly.",
    "Repeating their mistakes.",
    "Even in death.",
    "They never learn.",
    "They never give up.",
    "Why?",
    "What drives them?",
    "I gazed the stars.",
    "I studied their movements.",
    "I named all of them.",
    "I was unable to find any purpose in them.",
    "What is it that I...",
    "... We lack?",
    "Finally I realized it.",
    "Even the brightest star...",
    "Eventually burns out.",
    "Just like manusya.",
    "Their feeble life...",
    "Gave them meaning.",
    "Gave them purpose.",
    "Gave them a reason...",
    "To shine even brighter.",
    "Me and my sisters...",
    "We're unable...",
    "To bask in the light of the stars.",
    "Our very existence...",
    "Desecrates them.",
    "We're beings of dark.",
    "Beings of endless despair.",
    "Or so I thought.",
    "A wisftul feeling...",
    "Started to grow inside me.",
    "Was it hope?",
    "Love?",
    "Or something else?",
    "Add.",
    "I'm not sure...",
    "If this is the answer...",
    "... You were searching.",
    "It's all I have left now.",
    "I'll make sure you'll see it.",
    "Let me show you...",
    "Your evening star's light!",
]


for index, line in enumerate(LINES):
    with open(f"achievements/cif_fight_line_{str(index).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(number=index, line=line))