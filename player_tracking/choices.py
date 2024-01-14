HAND_CHOICES = [
    ("Left", "left"),
    ("Right", "right"),
    ("Both", "both"),
]

TRANSACTION_CHOICES = [
    ("Verbal Commitment from High School", "verbal"),
    ("Verbal Commitment from College", "transfer"),
    ("National Letter of Intent Signed", "nli"),
    ("Decommit", "decommit"),
    ("Entered Transfer Portal", "in_portal"),
    ("Signed Professional Contract", "pro"),
    ("No Longer With Program - Other Reason", "other"),
]

POSITION_CHOICES = [
    ("Pitcher", "P"),
    ("Catcher", "C"),
    ("First Base", "1B"),
    ("Second Base", "2B"),
    ("Third Base", "3B"),
    ("Shortstop", "SS"),
    ("Centerfield", "CF"),
    ("Corner Outfield", "OF"),
    ("Designated Hitter", "DH"),
]

STATUS_CHOICES = [
    ("Spring Roster", "roster"),
    ("Played but granted eligibility waiver", "waiver"),
    ("Roster not played", "redshirt"),
    ("Not on Spring roster", "greyshirt"),
]