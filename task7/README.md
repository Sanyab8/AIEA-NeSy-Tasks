
My implementation uses facts such as `plays(sanya, basketball)` and `plays(bob, soccer)`, along with rules such as `plays_indoor(X)` and `busy_player(X)`. The `plays_indoor(X)` rule checks whether a person plays a sport that is listed as indoor. The `busy_player(X)` rule checks whether a person plays two different sports. This helped me test both simple facts and more complex reasoning that depends on variables.

The main functions I implemented were `match`, `fill`, `prove`, `prove_options`, `prove_all`, and `prove_all_options`. The `match` function compares a goal or rule pattern against a fact and creates variable bindings. For example, matching `plays(X, Y)` with `plays(bob, soccer)` creates the bindings `X = bob` and `Y = soccer`. The `fill` function replaces variables with their known values. The `prove` function is the main function used to test whether a goal is true or false.

One important issue I ran into was that my first version of the code returned all `True` values, even for queries that should have been false. This happened because the program was proving each condition too separately and was not remembering variable values from one line of a rule to the next. For example, when proving `plays_indoor(bob)`, the old code could prove that Bob played some sport, but it forgot which sport Bob played before checking whether that sport was indoor. Because of this, the code reasoned incorrectly, almost like saying: “Bob plays some sport, and some indoor sport exists, so Bob plays an indoor sport.” That is not valid because the same variable `T` has to refer to the same sport throughout the whole rule.

The same issue happened with `busy_player(sanya)`. The rule checks whether Sanya plays two different sports using `plays(X, Y)`, `plays(X, Z)`, and `not_equal(Y, Z)`. In the old version, the code did not properly remember that both `Y` and `Z` became `basketball`, so it treated `Y` and `Z` like different symbols and returned true. After fixing the code, the program correctly keeps the bindings across the whole rule body. This means it checks `not_equal(basketball, basketball)`, which fails, so `busy_player(sanya)` correctly returns false.

I fixed this by adding helper functions that return possible bindings instead of only returning a boolean value. This allowed the program to carry variables like `T`, `Y`, and `Z` through the whole rule body. The corrected version does not just ask whether each condition is true somewhere; it asks what variable values make the condition true and then passes those same values into the next condition.

I tested the system using five queries in `main.py`. The first test was `plays_indoor(sanya)`, which returned `True` because Sanya plays basketball, and basketball is an indoor sport. The second test was `busy_player(bob)`, which returned `True` because Bob plays both soccer and baseball. The third test was `plays(sam, tennis)`, which returned `True` because it is a direct fact in the knowledge base. The fourth test was `plays_indoor(bob)`, which returned `False` because Bob plays soccer and baseball, and neither of those are listed as indoor sports. The fifth test was `busy_player(sanya)`, which returned `False` because Sanya only has one listed sport.

The final output of my test file was:

```text
True
True
True
False
False
```

This matched the expected results, so the backward chaining system was able to correctly reason over both facts and rules. Overall, this task helped me understand how symbolic reasoning systems use rules, variable matching, and bindings to prove logical statements.

GitHub repo: https://github.com/Sanyab8/AIEA-NeSy-Tasks
