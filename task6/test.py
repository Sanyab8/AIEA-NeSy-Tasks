import janus_swi as janus

janus.consult("zelda_kb.pl")

def test_zelda(query):
    result = janus.query_once(query)
    return result is not None

queries = [
    "japanese_game_company(legend_of_zelda)",
    "sell_more_than_one_million_copies(legend_of_zelda)",
    "top10_list(legend_of_zelda)"
]

for q in queries:
    print(f"{q} => {test_zelda(q)}")