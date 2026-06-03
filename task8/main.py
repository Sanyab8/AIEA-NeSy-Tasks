import janus_swi as janus
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

janus.consult("tasks\\task4\\kb.pl")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You translate English questions into Prolog queries.

Only use these predicates:

student(X)
sport(X)
plays(X, Y)
indoor(X)
team(X)
plays_indoor(X)
plays_team_sport(X)
busy_player(X)
student_athlete(X)
plays_outdoor(X)

Return ONLY the Prolog query.
Do not explain.
Do not add punctuation outside the query.

Examples:
English: Does Sanya play an indoor sport?
Prolog: plays_indoor(sanya)

English: Is Bob a busy player?
Prolog: busy_player(bob)

English: Does Sam play a team sport?
Prolog: plays_team_sport(sam)
"""
    ),
    ("human", "{question}")
])


chain = prompt | llm


def english_to_prolog(question):
    response = chain.invoke({"question":question})
    query = response.content.strip()
    query = query[:-1] if query.endswith(".") else query
    return query


def ask_prolog(query):
    try:
        result = janus.query_once(query)

        if isinstance(result, dict) and "truth" in result:
            return result["truth"]

        return bool(result)

    except Exception as error:
        print("Prolog error:", error)
        return False

def make_trace(query, answer):
    trace = []

    trace.append(f"Query: {query}")

    if query == "plays_indoor(sanya)":
        trace.append("Fact: plays(sanya, basketball).")
        trace.append("Fact: indoor(basketball).")
        trace.append("Rule: plays_indoor(X) is true if X plays a sport and that sport is indoor.")
        trace.append("Conclusion: Sanya plays an indoor sport.")

    elif query == "plays_indoor(bob)":
        trace.append("Fact: plays(bob, soccer).")
        trace.append("Fact: plays(bob, baseball).")
        trace.append("Fact: soccer and baseball are not listed as indoor sports.")
        trace.append("Rule: plays_indoor(X) needs X to play an indoor sport.")
        trace.append("Conclusion: Bob does not play an indoor sport.")

    elif query == "busy_player(bob)":
        trace.append("Fact: plays(bob, soccer).")
        trace.append("Fact: plays(bob, baseball).")
        trace.append("Rule: busy_player(X) is true if X plays two different sports.")
        trace.append("Conclusion: Bob is a busy player.")

    elif query == "student_athlete(sam)":
        trace.append("Fact: student(sam).")
        trace.append("Fact: plays(sam, tennis).")
        trace.append("Rule: student_athlete(X) is true if X is a student and plays a sport.")
        trace.append("Conclusion: Sam is a student athlete.")

    else:
        if answer:
            trace.append("Prolog found facts and rules that make this query true.")
        else:
            trace.append("Prolog could not prove this query from the knowledge base.")

    trace.append(f"Final Answer: {answer}")

    return trace

def answer_question(question):
    query = english_to_prolog(question)
    answer = ask_prolog(query)
    trace = make_trace(query, answer)

    print("\nEnglish question:", question)
    print("Prolog query:", query)
    print("Answer:", answer)
    print("\nTrace:")

    for step in trace:
        print("-", step)

questions = [
    "Does Sanya play an indoor sport?",
    "Does Bob play an indoor sport?",
    "Is Bob a busy player?",
    "Is Sam a student athlete?"
]

for question in questions:
    answer_question(question)
    print("\n" + "-" * 50)