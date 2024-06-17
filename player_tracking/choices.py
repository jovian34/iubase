HAND_CHOICES = [
    ("Left", "Left"),
    ("Right", "Right"),
    ("Both", "Both"),
]

JOINED_TUPLES = [
    ("Verbal Commitment from High School", "Verbal Commitment from High School"),
    ("Verbal Commitment from College", "Verbal Commitment from College"),
    ("National Letter of Intent Signed", "National Letter of Intent Signed"),
    ("Not Drafted", "Not Drafted"),
    ("Not Signing Professional Contract", "Not Signing Professional Contract"),
]

LEFT_TUPLES = [
    ("Decommit", "Decommit"),
    ("Entered Transfer Portal", "Entered Transfer Portal"),
    ("Verbal Commitment to Transfer College", "Verbal Commitment to Transfer College"),
    ("Attending MLB Draft Combine", "Attending MLB Draft Combine"),
    ("Drafted", "Drafted"),
    ("Signed Professional Contract", "Signed Professional Contract"),
    ("No Longer With Program - Other Reason", "No Longer With Program - Other Reason"),
]

TRANSACTION_CHOICES = JOINED_TUPLES + LEFT_TUPLES
LEFT = [ left_tuple[0] for left_tuple in LEFT_TUPLES ]
JOINED = [ joined_tuple[0] for joined_tuple in JOINED_TUPLES ]

POSITION_CHOICES = [
    ("Pitcher", "Pitcher"),
    ("Catcher", "Catcher"),
    ("First Base", "First Base"),
    ("Second Base", "Second Base"),
    ("Third Base", "Third Base"),
    ("Shortstop", "Shortstop"),
    ("Centerfield", "Centerfield"),
    ("Corner Outfield", "Corner Outfield"),
    ("Designated Hitter", "Designated Hitter"),
    (None, "None")
]

ROSTERED_TUPLES = [
    ("Fall Roster", "Fall Roster"),
    ("Spring Roster", "Spring Roster"),
]

GREY_SHIRT_TUPLES = [
    ("Not on Spring roster", "Not on Spring roster"),
]

RED_SHIRT_TUPLES = [
    ("Played but granted eligibility waiver", "Played but granted eligibility waiver"),
    ("On Spring Roster but did not play", "On Spring Roster but did not play"),
    ("Replaced on Spring Roster - Medical", "Replaced on Spring Roster - Medical"),
]

RED_SHIRT_PLUS_WAIVER_TUPLES = [
    ("Redshirt with clock extension - Medical", "Redshirt with clock extension - Medical"),
    ("Redshirt with clock extension - Other", "Redshirt with clock extension - Other"),
]

STATUS_CHOICES = ROSTERED_TUPLES + GREY_SHIRT_TUPLES + RED_SHIRT_TUPLES + RED_SHIRT_PLUS_WAIVER_TUPLES
ROSTERED = [ rostered_tuple[0] for rostered_tuple in ROSTERED_TUPLES ]
GREY_SHIRT = [ grey_shirt_tuple[0] for grey_shirt_tuple in GREY_SHIRT_TUPLES ]
RED_SHIRT = [ red_shirt_tuple[0] for red_shirt_tuple in RED_SHIRT_TUPLES ]
RED_SHIRT_PLUS_WAIVER = [ red_shirt_waiver_tuple[0] for red_shirt_waiver_tuple in RED_SHIRT_PLUS_WAIVER_TUPLES ]
