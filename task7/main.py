from backwardchain import prove

print(prove(("plays_indoor", "sanya")))     # True  - basketball is indoor
print(prove(("busy_player", "bob")))        # True  - plays soccer AND baseball
print(prove(("plays", "sam", "tennis")))    # True  - direct fact
print(prove(("plays_indoor", "bob")))       # False - soccer+baseball not indoor
print(prove(("busy_player", "sanya")))      # False - only plays basketball