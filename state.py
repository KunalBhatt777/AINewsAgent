from typing import TypedDict, List

class AgentState(TypedDict):
    topic: str               # user's input topic
    sub_queries: List[str]   # planner's output
    raw_results: List[dict]  # search results from Tavily
    deduped: List[dict]      # after removing duplicates
    report: str              # final briefing