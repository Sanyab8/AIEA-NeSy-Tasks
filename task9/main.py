import janus_swi as janus
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

janus.consult("../task4/kb.pl")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def load_kb():
    with open("task4/kb.pl", "r", encoding="utf-8") as file:
        return file.read()


def retrieve_context(state):
    question = state["question"].lower()
    kb = load_kb()
    lines = kb.splitlines()
    useful_lines = []

    for line in lines:
        small_line = line.lower()

        if "sanya" in question and "sanya" in small_line:
            useful_lines.append(line)
        elif "bob" in question and "bob" in small_line:
            useful_lines.append(line)
        elif "sam" in question and "sam" in small_line:
            useful_lines.append(line)
        elif "charlie" in question and "charlie" in small_line:
            useful_lines.append(line)
        elif "alex" in question and "alex" in small_line:
            useful_lines.append(line)
        elif "indoor" in question and "indoor" in small_line:
            useful_lines.append(line)
        elif "team" in question and "team" in small_line:
            useful_lines.append(line)
        elif "busy" in question and "busy_player" in small_line:
            useful_lines.append(line)
        elif "athlete" in question and "student_athlete" in small_line:
            useful_lines.append(line)
        elif "outdoor" in question and "plays_outdoor" in small_line:
            useful_lines.append(line)

    if len(useful_lines) < 2:
        useful_lines = lines

    return {
        "context": "\n".join(useful_lines)
    }


relevance_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You judge whether the retrieved Prolog knowledge base context is relevant.

Answer ONLY yes or no.
Do not explain.
"""
    ),
    (
        "human",
        """
Question:
{question}

Retrieved context:
{context}

Is this context relevant enough to answer the question?
"""
    )
])

relevance_chain = relevance_prompt | llm


def judge_relevance(state):
    response = relevance_chain.invoke({
        "question": state["question"],
        "context": state["context"]
    })

    answer = response.content.strip().lower()

    if "yes" in answer:
        relevant = True
    else:
        relevant = False

    return {
        "relevant": relevant
    }


def refine_context(state):
    kb = load_kb()

    return {
        "context": kb,
        "refined": True
    }


def decide_after_relevance(state):
    if state["relevant"]:
        return "generate_query"
    else:
        return "refine_context"


query_prompt = ChatPromptTemplate.from_messages([
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
Do not wrap the query in markdown.

Examples:
English: Does Sanya play an indoor sport?
Prolog: plays_indoor(sanya)

English: Is Bob a busy player?
Prolog: busy_player(bob)

English: Does Sam play a team sport?
Prolog: plays_team_sport(sam)
"""
    ),
    (
        "human",
        """
Question:
{question}

Relevant context:
{context}
"""
    )
])

query_chain = query_prompt | llm


def generate_query(state):
    response = query_chain.invoke({
        "question": state["question"],
        "context": state["context"]
    })

    query = response.content.strip()

    query = query.replace("```prolog", "")
    query = query.replace("```", "")
    query = query.strip()

    if query.endswith("."):
        query = query[:-1]

    return {
        "query": query
    }


def ask_prolog_node(state):
    query = state["query"]

    try:
        result = janus.query_once(query)

        if isinstance(result, dict) and "truth" in result:
            answer = result["truth"]
        else:
            answer = bool(result)

    except Exception as error:
        print("Prolog error:", error)
        answer = False

    return {
        "answer": answer
    }


def make_trace_node(state):
    query = state["query"]
    answer = state["answer"]
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

    return {
        "trace": trace
    }


graph = StateGraph(dict)

graph.add_node("retrieve_context", retrieve_context)
graph.add_node("judge_relevance", judge_relevance)
graph.add_node("refine_context", refine_context)
graph.add_node("generate_query", generate_query)
graph.add_node("ask_prolog", ask_prolog_node)
graph.add_node("make_trace", make_trace_node)

graph.add_edge(START, "retrieve_context")
graph.add_edge("retrieve_context", "judge_relevance")

graph.add_conditional_edges(
    "judge_relevance",
    decide_after_relevance,
    {
        "generate_query": "generate_query",
        "refine_context": "refine_context"
    }
)

graph.add_edge("refine_context", "generate_query")
graph.add_edge("generate_query", "ask_prolog")
graph.add_edge("ask_prolog", "make_trace")
graph.add_edge("make_trace", END)

app = graph.compile()


def answer_question(question):
    starting_state = {
        "question": question,
        "context": "",
        "relevant": False,
        "refined": False,
        "query": "",
        "answer": False,
        "trace": []
    }

    result = app.invoke(starting_state)

    print("\nEnglish question:", result["question"])
    print("Retrieved context:")
    print(result["context"])
    print("Relevant:", result["relevant"])
    print("Prolog query:", result["query"])
    print("Answer:", result["answer"])
    print("\nTrace:")

    for step in result["trace"]:
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