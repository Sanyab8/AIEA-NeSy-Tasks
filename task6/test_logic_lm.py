import subprocess

def ask_prolog(query):
    command = f"consult('kb.pl'), ({query} -> writeln(true); writeln(false)), halt."

    result = subprocess.run(
        ["swipl", "-q", "-g", command],
        capture_output=True, text=True
    )
    if result.stderr:
        return "Error" + result.stderr.strip()
    
query = "top10_list(legend_of_zelda)"
result = ask_prolog(query)

print("Logic-LM Paper Example: Zelda")
print("--------------------------------")
print("Premise: sell_more_than_one_million_copies(legend_of_zelda)")
print("Rule: If a game sells more than one million copies, then it is in the Top 10 list.")
print("Query:", query)

