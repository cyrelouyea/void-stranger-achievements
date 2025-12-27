FORMAT = """title: {lyric}
description: Listen to Voided

"""

FORMAT_ADD = """// PATCH gml_Object_obj_voidsong_Step_0 {linenumber}
{{-achievement}}
{{+achievement}}
"""

LYRICS = [
    ("There's a safety locker", 170),
    ("inside of me", 177),
    ("out of your reach", 187),
    ("And I hold the key", 192),
    ("It's sealed with layers", 202),
    ("and layers of irony", 207),
    ("What's within", 217),
    ("I refuse to see", 221),
    ("I hold on I hold on I hold on", 231),
    ("'cause that's the only thing", 241),
    ("the one thing that I can control", 245),
    ("My grievance is mine", 249),
    ("My sadness is mine", 253),
    ("My loss is mine", 257),
    ("One toss and I'll forever be blind", 268),
    ("Toss the key oh please be kind", 272),
    ("In this state of oblivion", 282),
    ("My silence goes on", 286),
    ("My bearings stay stored", 290),
    ("My walls stay strong", 294),
    ("I hold on I hold on I hold on", 304),
    ("'cause that's the only thing", 314),
    ("the one thing that I can control", 318),
    ("My grievance is mine", 322),
    ("My sadness is mine", 326),
    ("My loss is mine", 330),
    ("I hold on I hold on I hold on", 342),
    ("'cause that's the only thing", 352),
    ("the one thing that I can control", 356),
    ("My grievance is mine", 366),
    ("My sadness is mine", 370),
    ("My loss is mine", 374),
    ("My grievance is mine", 384),
    ("My sadness is mine", 388),
    ("My loss is mine", 392)
]

lyrics_done = {}
number = 1
for  (lyric, linenumber) in LYRICS:
    if lyric in lyrics_done:
        file_number = lyrics_done[lyric]
        with open(f"achievements/voided_lyrics_{str(file_number).rjust(2, '0')}", "a") as f:
            f.write(FORMAT_ADD.format(
                linenumber=linenumber
            ))
    else:
        with open(f"achievements/voided_lyrics_{str(number).rjust(2, '0')}", "w") as f:
            f.write(FORMAT.format(
                lyric=lyric,
            ))
            f.write(FORMAT_ADD.format(
                linenumber=linenumber
            ))
        
        lyrics_done[lyric] = number
        number += 1
    
    
