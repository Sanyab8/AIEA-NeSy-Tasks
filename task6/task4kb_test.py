import janus_swi as janus

janus.consult("../task4/kb.pl")


def test_query(query):
    try:
        result = janus.query_once(query)
        if isinstance(result, dict) and "truth" in result:
            return result["truth"]
        return bool(result)
    
    except Exception as e:
        return f"ERROR: {e}"



tests = [
    {
        "english": "Does Sanya play an indoor sport?",
        "logic_query": "plays_indoor(sanya)",
        "expected": True,
    },
    {
        "english": "Does Bob play an indoor sport?",
        "logic_query": "plays_indoor(bob)",
        "expected": False,
    },
    {
        "english": "Is Bob a busy player?",
        "logic_query": "busy_player(bob)",
        "expected": True,
    },
    {
        "english": "Is Sam a busy player?",
        "logic_query": "busy_player(sam)",
        "expected": False,
    },
]

for test in tests:
    result = test_query(test["logic_query"])

    if result == test["expected"]:
        status = "PASSED"
    else:
        status = "FAILED"

    print("English question:", test["english"])
    print("Logic query:", test["logic_query"])
    print("Prolog result:", result)
    print("Expected:", test["expected"])
    print("Got:", result)
    print("Test:", status)
    print()
    
