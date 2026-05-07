from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import planner_node, search_node, dedup_node, report_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("dedup", dedup_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "dedup")
    graph.add_edge("dedup", "report")
    graph.add_edge("report", END)

    return graph.compile()


app = build_graph()
