HAND = [
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
    ("Ranked MLB Draft Prospect for Next Draft", "Ranked MLB Draft Prospect for Next Draft"),
    ("Drafted", "Drafted"),
    (
        "Signed Professional Contract - Undrafted",
        "Signed Professional Contract - Undrafted",
    ),
    ("Medical Waiver - ending eligibility", "Medical Waiver - ending eligibility"),
    ("No Longer With Program - Other Reason", "No Longer With Program - Other Reason"),
    (
        "Not playing but with the program in another role",
        "Not playing but with the program in another role",
    ),
]

AFTER_TUPLES = [
    ("Drafted former IU", "Drafted former IU"),
    ("Signed Professional Contract", "Signed Professional Contract"),
    ("Verbal Commitment to New College", "Verbal Commitment to New College"),
    ("Entered Transfer Portal - former IU", "Entered Transfer Portal - former IU"),
]

TRANSACTIONS = JOINED_TUPLES + LEFT_TUPLES + AFTER_TUPLES
LEFT = [left_tuple[0] for left_tuple in LEFT_TUPLES]
JOINED = [joined_tuple[0] for joined_tuple in JOINED_TUPLES]
AFTER = [after_tuple[0] for after_tuple in AFTER_TUPLES]
COLLEGE = [JOINED_TUPLES[1][0]]
HS = [JOINED_TUPLES[0][0], JOINED_TUPLES[2], [0]]

POSITIONS = [
    ("Pitcher", "Pitcher"),
    ("Catcher", "Catcher"),
    ("First Base", "First Base"),
    ("Second Base", "Second Base"),
    ("Third Base", "Third Base"),
    ("Shortstop", "Shortstop"),
    ("Centerfield", "Centerfield"),
    ("Corner Outfield", "Corner Outfield"),
    ("Designated Hitter", "Designated Hitter"),
    (None, "None"),
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
    ("Medical Waiver - ending eligibility", "Medical Waiver - ending eligibility"),
    ("Replaced on Spring Roster - Medical", "Replaced on Spring Roster - Medical"),
]

RED_SHIRT_PLUS_WAIVER_TUPLES = [
    (
        "Redshirt with clock extension - Medical",
        "Redshirt with clock extension - Medical",
    ),
    ("Redshirt with clock extension - Other", "Redshirt with clock extension - Other"),
]

STATUS_CHOICES = (
    ROSTERED_TUPLES
    + GREY_SHIRT_TUPLES
    + RED_SHIRT_TUPLES
    + RED_SHIRT_PLUS_WAIVER_TUPLES
)
ROSTERED = [rostered_tuple[0] for rostered_tuple in ROSTERED_TUPLES]
GREY_SHIRT = [grey_shirt_tuple[0] for grey_shirt_tuple in GREY_SHIRT_TUPLES]
RED_SHIRT = [red_shirt_tuple[0] for red_shirt_tuple in RED_SHIRT_TUPLES]
RED_SHIRT_PLUS_WAIVER = [
    red_shirt_waiver_tuple[0] for red_shirt_waiver_tuple in RED_SHIRT_PLUS_WAIVER_TUPLES
]
ALL_ROSTER = [ROSTERED_TUPLES[1][0], RED_SHIRT_TUPLES[1][0], RED_SHIRT_TUPLES[0][0]]
