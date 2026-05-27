import janus_swi as janus

janus.consult("../task4/kb.pl")

def test_query(query):
    result = janus.query_once(query)
    return result is not None

tests = [
    "student(sanya)",
    "plays(bob,soccer)",
    "busy_player(bob)",
    "busy_player(sanya)",
    "plays_indoor(sanya)",
    "plays_indoor(bob)"
]

for query in tests:
    print(f"{query} => {test_query(query)}")