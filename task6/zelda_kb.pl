japanese_game_company(legend_of_zelda).
sell_more_than_one_million_copies(legend_of_zelda).

top10_list(X) :-
    sell_more_than_one_million_copies(X).