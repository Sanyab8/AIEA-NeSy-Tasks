from kb import facts, rules

def is_var(x):
    return isinstance(x, str) and x.isupper()

def match(pattern, fact, bindings=None):
    if bindings is None:
        bindings = {}

    if len(pattern) != len(fact):
        return None

    new_bindings = bindings.copy()

    for p, f in zip(pattern, fact):
        # If p is already bound, use its value
        if is_var(p) and p in new_bindings:
            p = new_bindings[p]

        # If f is already bound, use its value
        if is_var(f) and f in new_bindings:
            f = new_bindings[f]

        if is_var(p):
            new_bindings[p] = f
        elif is_var(f):
            new_bindings[f] = p
        elif p != f:
            return None

    return new_bindings

def fill(term, bindings):
    # fill(("plays", "X", "T"), {"X": "bob", "T": "soccer"})
    # becomes ("plays", "bob", "soccer")
    return tuple(bindings.get(x, x) for x in term)

def prove(goal, bindings=None):  # backward chain
    if bindings is None:
        bindings = {}

    return len(prove_options(goal, bindings)) > 0

def prove_options(goal, bindings=None):
    if bindings is None:
        bindings = {}

    goal = fill(goal, bindings)
    results = []

    # Try direct facts
    for fact in facts:
        new_bindings = match(goal, fact, bindings)
        if new_bindings is not None:
            results.append(new_bindings)

    # Try rules
    for rule in rules:
        new_bindings = match(rule["head"], goal, bindings)

        if new_bindings is None:
            continue

        body_results = prove_all_options(rule["body"], new_bindings)
        results.extend(body_results)

    return results

def prove_all(conditions, bindings):
    return len(prove_all_options(conditions, bindings)) > 0

def prove_all_options(conditions, bindings):
    # If there are no more conditions, this path worked
    if len(conditions) == 0:
        return [bindings]

    condition = fill(conditions[0], bindings)
    rest = conditions[1:]

    # Special case for Y != Z
    if condition[0] == "not_equal":
        if condition[1] == condition[2]:
            return []
        return prove_all_options(rest, bindings)

    results = []

    # Try every possible way to prove this condition
    for new_bindings in prove_options(condition, bindings):
        results.extend(prove_all_options(rest, new_bindings))

    return results