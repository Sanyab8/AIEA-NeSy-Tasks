Title: Logic-LM Local Reimplementation Writeup

1. Paper chosen
I chose Logic-LM because it directly matches the goal of the LLM logic project: translating natural language reasoning problems into symbolic logic and using a solver to check the answer.

2. Tools installed
I used Python and SWI-Prolog locally. Python handled the test runner, and SWI-Prolog acted as the symbolic reasoning engine.

3. What I implemented
I reimplemented the core Logic-LM idea at a small scale. Instead of relying on the LLM for every translation step, I manually wrote the logic program from the natural language problem, then used Prolog to test whether the conclusion followed from the premises.

4. Test KB
I tested the system on the Zelda KB:
- sell_more_than_one_million_copies(legend_of_zelda).
- top10_list(X) :- sell_more_than_one_million_copies(X).

5. Test result
The query top10_list(legend_of_zelda). returned true, which matches the expected answer. The conclusion is true because the KB contains a rule saying that any game that sells more than one million copies is selected into the Top 10 list.

6. What I learned
The symbolic solver is reliable once the rules are written correctly. The main challenge is translating natural language into the right predicates, constants, and rules. Small typos, like writing legend_of_zelds instead of legend_of_zelda, break the reasoning even when the logic idea is correct.

7. GitHub repo
https://github.com/Sanyab8/AIEA-NeSy-Tasks
