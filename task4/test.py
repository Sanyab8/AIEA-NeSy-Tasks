import janus_swi as janus

janus.consult("kb.pl")

queries = [
    "student(sanya)",
    "plays(sanya, basketball)",
    "plays(bob, soccer)",
    "busy_player(bob)",
    "busy_player(sanya)",
    "plays_indoor(sanya)",
    "plays_indoor(bob)"
]

for q in queries:
    result = janus.query_once(q)
    print(q, "=>", result)

print("\nBusy players:")
for result in janus.query("busy_player(X)"):
    print(result)

print("\nIndoor players:")
for result in janus.query("plays_indoor(X)"):
    print(result)