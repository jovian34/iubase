INNING_PART_CHOICES = [
    ("Top", "Top"),
    ("Bottom", "Bottom"),
]

GAME_STATUS = [
    ("pre-game", "game not started"),
    ("in-progress", "game in progress"),
    ("cancelled", "cancelled"),
    ("delay", "mid-game delay"),
    ("final", "game concluded"),
    ("post-game", "post-game"),
]

OUTS_CHOICES = [
    (0, "none"),
    (1, "one"),
    (2, "two"),
    (3, "three"),
]

TIMEZONE_CHOICES = [
    ("America/New_York", "Eastern"),
    ("America/Chicago", "Central"),
    ("America/Denver", "Mountain"),
    ("America/Phoenix", "Arizona"),
    ("America/Los_Angeles", "Pacific"),
    ("America/Honolulu", "Hawaii"),
]

SURFACE_CHOICES = [
    ("natural", "natural"),
    ("artificial", "artificial"),
]

DUGOUT_CHOICES = [
    ("third", "third"),
    ("first", "first"),
]