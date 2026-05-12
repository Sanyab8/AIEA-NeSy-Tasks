# Datalog Logic Tutorial

Datalog is a declarative query language based on logic programming. Instead of writing step-by-step instructions like in traditional programming, you describe relationships between data and let the engine infer the results. It is similar to SQL, but it handles relationships and recursion much more naturally. 

## Basic Structure

Datalog works using predicates and data patterns.

A data pattern looks like:

[entity attribute value]

Example:

```
[?person :lives-in ?city]
```

This means:

* some person lives in some city

Variables start with `?`.

Queries are usually written with `:find` and `:where`.

Example:

```clojure
[:find ?name
 :where
 [?person :first-name ?name]]
```

This retrieves all names that satisfy the conditions in the `:where` block. 

---

# Rules

Rules let you define reusable logic.

Example rule:

```clojure
[(lives-in-country ?person ?country)
 [?person :lives-in ?city]
 [?city :located-in ?country]]
```

This rule says:

> A person lives in a country if they live in a city and that city is located in the country.

You can then use the rule inside a query:

```clojure
[:find ?name
 :where
 [?person :first-name ?name]
 (lives-in-country ?person "France")]
```

This finds all people who live in France. 

---

# Constraints

Datalog can also apply constraints using predicates such as `contains?`.

Example:

```clojure
[(lives-in-country-whitelisted ?person ?country)
 [?person :lives-in ?city]
 [?city :located-in ?country]
 [(contains? #{"Paris" "Lyon"} ?city)]]
```

This adds a restriction:

* the city must be either Paris or Lyon

So the rule only succeeds if the person lives in one of those cities. 

---

# Recursion

One of Datalog’s biggest strengths is recursion.

Example:

```clojure
[(genealogy ?person ?ancestor)
 (parent-of ?person ?ancestor)]

[(genealogy ?person ?ancestor)
 (parent-of ?person ?ancestor-1)
 (genealogy ?ancestor-1 ?ancestor)]
```

The first rule is the **base case**:

* a parent is an ancestor

The second rule is the **recursive case**:

* if your parent has an ancestor, then that ancestor is also your ancestor

This allows Datalog to automatically traverse family trees and graph structures. 

Example query:

```clojure
[:find [?person ?great-grand-parent]
 :where
 (genealogy ?person ?parent)
 (genealogy ?parent ?grand-parent)
 (genealogy ?grand-parent ?great-grand-parent)]
```

This finds great-grandparents by repeatedly following ancestor relationships.

---

# Why Datalog?

Advantages:

* cleaner and simpler logic than SQL
* reusable rules
* strong support for recursive and graph-like data
* easier handling of complex relationships 

Limitations:

* less mainstream adoption
* fewer tools and integrations
* historical performance concerns 

Overall, Datalog is especially useful for graph traversal, relationship-heavy systems, recursive queries, and semi-structured data.

SlideShow: https://docs.google.com/presentation/d/15GvQZuiKycRkzZaF1VDLLawLbYMPmE8aObZxkpzS-LQ/edit?slide=id.g2576a45fa49_2_87#slide=id.g2576a45fa49_2_87

