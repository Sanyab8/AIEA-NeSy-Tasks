i couldn't find a code in paper so I am using one of the examples.


Problem:A Japanese game company created the game the Legend of Zelda. All games in the Top 10 list are made by Japanese game companies. If a 
game sells more than one million copies, then it will be selected into the Top 10 list. The Legend of Zelda sold more than one million copies.
Question: Based on the above information, is the following statement true, false, or uncertain? The Legend of Zelda is in the Top 10 list.
(A) True                (B) False            (C) Uncertain
Predicted logic programs:
Premises:
JapaneseGameCompany(legend_of_zelda)
∀x (Top10List(x) → JapaneseGameCompany(x))
∀x (SellMoreThanOneMillionCopies(x)→ Top10List(x))
SellMoreThanOneMillionCopies(legend_of_zelda)
Conclusion:
Top10List(legend_of_zelda)
Predicted answer: A