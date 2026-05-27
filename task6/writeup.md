Title: Logic-LM Local Reimplementation Writeup

For this task, I chose Logic-LM because it directly connects to the goal of the LLM logic project: translating natural language reasoning problems into symbolic logic and using a solver to check whether the answer follows from the given facts and rules.

I used Python, SWI-Prolog, and Janus locally. SWI-Prolog acted as the symbolic reasoning engine, while Python acted as the test runner and result interpreter. Janus connected Python to SWI-Prolog so that my Python script could load a Prolog knowledge base, send queries, and read the result.

For my reimplementation, I recreated the core Logic-LM idea at a smaller scale. Logic-LM’s full pipeline uses an LLM to translate natural language into a symbolic form, then uses a logic solver to reason over that symbolic form. In my version, I manually wrote the symbolic logic in Prolog, then used Python and Janus to test whether the conclusions followed from the knowledge base. This still follows the main structure of the paper: natural language question → symbolic query → solver result → interpreted answer.

I tested my implementation using the same Prolog knowledge base from Task 4. The KB included facts about students, sports, which sports each student plays, and whether a sport is indoor or team-based. It also included rules such as `plays_indoor(X) :- plays(X, T), indoor(T).` and `busy_player(X) :- plays(X, Y), plays(X, Z), Y \= Z.` These rules allowed Prolog to infer new information instead of only checking direct facts.

My Python test script loaded the Task 4 KB using Janus and ran queries such as `plays_indoor(sanya)`, `plays_indoor(bob)`, `busy_player(bob)`, and `busy_player(sam)`. The script compared each Prolog result to an expected answer and printed whether the test passed or failed. For example, `plays_indoor(sanya)` returned true because Sanya plays basketball and basketball is listed as an indoor sport. `busy_player(bob)` also returned true because Bob plays two different sports: soccer and baseball. On the other hand, `plays_indoor(bob)` returned false because Bob’s sports were not listed as indoor sports, and `busy_player(sam)` returned false because Sam only had one sport in the KB.

This helped me understand why symbolic reasoning is useful for LLM logic work. Once the facts and rules are written correctly, Prolog gives consistent answers based on the knowledge base instead of guessing. The main challenge is translating the original natural language into the right predicates, constants, and rules. Small mistakes in predicate names, file paths, or constants can break the reasoning even when the overall idea is correct.

GitHub repo: https://github.com/Sanyab8/AIEA-NeSy-Tasks