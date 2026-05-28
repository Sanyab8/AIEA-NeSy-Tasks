facts = [
    ("student", "sanya"),
    ("student", "bob"),
    ("student", "sam"),
    ("student", "charlie"),
    ("student", "alex"),

    ("sport", "badminton"),
    ("sport", "soccer"),
    ("sport", "baseball"),
    ("sport", "basketball"),
    ("sport", "tennis"),

    ("plays", "sanya", "basketball"),
    ("plays", "bob", "soccer"),
    ("plays", "sam", "tennis"),
    ("plays", "alex", "tennis"),
    ("plays", "bob", "baseball"),

    ("indoor", "badminton"),
    ("indoor", "basketball"),

    ("team", "soccer"),
    ("team", "baseball"),
    ("team", "basketball"),
]

rules = [
    {
        "head": ("busy_player", "X"),
        "body": [
            ("plays", "X", "Y"),
            ("plays", "X", "Z"),
            ("not_equal", "Y", "Z")
        ]
    },

    {
        "head": ("plays_indoor", "X"),
        "body": [
            ("plays", "X", "T"),
            ("indoor", "T")
        ]
    }
]