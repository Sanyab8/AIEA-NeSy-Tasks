student(sanya).
student(bob).
student(sam).
student(charlie).
student(alex).

sport(badminton).
sport(soccer).
sport(baseball).
sport(basketball).
sport(tennis).

plays(sanya, basketball).
plays(bob, soccer).
plays(sam, tennis).
plays(alex, tennis).
plays(bob, baseball).

indoor(badminton).
indoor(basketball).

team(soccer).
team(baseball).
team(basketball).

busy_player(X) :-
    plays(X, Y),
    plays(X, Z),
    Y \= Z.

plays_indoor(X) :-
    plays(X, T),
    indoor(T).