from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from state import AgentState
from llm import llm
from tools import search

# --- Prompt Templates ---

planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a research planner specializing in generating targeted news search queries. "
        "Your output must be exactly 4 concise, distinct search queries—one per line, "
        "no numbering, no bullets, no extra text."
    ),
    (
        "human",
        "Generate 4 search queries to find comprehensive recent news coverage on: {topic}"
    ),
])

report_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior news analyst who writes clear, well-structured briefings. "
        "Always format your response with these three sections:\n\n"
        "## Executive Summary\n"
        "2-3 sentences capturing the overall picture.\n\n"
        "## Key Developments\n"
        "Bullet points covering the most important findings.\n\n"
        "## Notable Sources\n"
        "List article titles with their URLs.\n\n"
        "Be factual, concise, and cite sources by title."
    ),
    (
        "human",
        "Write a comprehensive news briefing on the topic: {topic}\n\n"
        "Use the following articles as your sources:\n\n{articles}"
    ),
])

# --- LCEL Runnable Chains ---

planner_chain = planner_prompt | llm | StrOutputParser()
report_chain = report_prompt | llm | StrOutputParser()


# --- Graph Nodes ---

def planner_node(state: AgentState) -> AgentState:
    output = planner_chain.invoke({"topic": state["topic"]})
    queries = [q.strip() for q in output.strip().split("\n") if q.strip()]
    return {"sub_queries": queries}


def search_node(state: AgentState) -> AgentState:
    raw_results = []
    for query in state["sub_queries"]:
        results = search(query)
        for r in results:
            r["query"] = query
        raw_results.extend(results)
    return {"raw_results": raw_results}


def dedup_node(state: AgentState) -> AgentState:
    seen_urls = set()
    deduped = []
    for item in state["raw_results"]:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            deduped.append(item)
    return {"deduped": deduped}


def report_node(state: AgentState) -> AgentState:
    articles_text = "\n\n".join(
        f"Title: {a.get('title', 'N/A')}\nURL: {a.get('url', 'N/A')}\nSummary: {a.get('content', 'N/A')}"
        for a in state["deduped"]
    )
    report = report_chain.invoke({"topic": state["topic"], "articles": articles_text})
    return {"report": report.strip()}
