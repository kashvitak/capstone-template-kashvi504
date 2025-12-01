from typing import TypedDict, List
from langgraph.graph import END, StateGraph, START
from IPython.display import Image, display

# Define the state (Mocking for the example)
class OverallState(TypedDict):
    topic: str
    fact: str

# Define dummy nodes
def generate_topics(state: OverallState):
    return {"topic": "cats"}

def generate_fact(state: OverallState):
    return {"fact": "Cats sleep a lot."}

def best_fact(state: OverallState):
    return {"fact": "Cats are liquid."}

def continue_to_facts(state: OverallState):
    return ["generate_fact"]

# --- YOUR CODE STARTS HERE ---

# Construct the graph: here we put everything together to construct our graph
graph = StateGraph(OverallState)
graph.add_node("generate_topics", generate_topics)
graph.add_node("generate_fact", generate_fact)
graph.add_node("best_fact", best_fact)
graph.add_edge(START, "generate_topics")
graph.add_conditional_edges("generate_topics", continue_to_facts, ["generate_fact"])
graph.add_edge("generate_fact", "best_fact")
graph.add_edge("best_fact", END)

# Compile the graph
app = graph.compile()

# Visualize
try:
    print("Generating graph image...")
    # If running in a notebook, use: display(Image(app.get_graph().draw_mermaid_png()))
    # For script, we'll save it
    png_data = app.get_graph().draw_mermaid_png()
    with open("simple_graph_example.png", "wb") as f:
        f.write(png_data)
    print("Graph saved to simple_graph_example.png")
except Exception as e:
    print(f"Could not draw graph: {e}")
