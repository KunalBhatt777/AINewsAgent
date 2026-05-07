import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from agent import app

st.set_page_config(
    page_title="AI News Briefing Agent",
    page_icon="📰",
    layout="wide",
)

st.title("📰 AI News Briefing Agent")
st.caption("Powered by LangGraph · Claude Haiku 4.5 on AWS Bedrock · Tavily Search")

st.divider()

topic = st.text_input(
    label="Enter a topic to research:",
    placeholder="e.g. generative AI in healthcare 2025",
)

run = st.button("Generate Briefing", type="primary", disabled=not topic.strip())

if run and topic.strip():
    # Stream node-by-node so we can show live progress
    step_status = st.status("Running agent...", expanded=True)

    final_state = {}

    with step_status:
        for chunk in app.stream({"topic": topic.strip()}, stream_mode="updates"):
            node_name = next(iter(chunk))
            node_output = chunk[node_name]
            final_state.update(node_output)

            if node_name == "planner":
                st.write("**Planner** — search queries generated")
            elif node_name == "search":
                st.write(f"**Search** — {len(node_output.get('raw_results', []))} raw articles fetched")
            elif node_name == "dedup":
                st.write(f"**Dedup** — {len(node_output.get('deduped', []))} unique articles kept")
            elif node_name == "report":
                st.write("**Report** — briefing written")

        step_status.update(label="Done!", state="complete", expanded=False)

    st.divider()

    # Sub-queries
    with st.expander("Search queries used", expanded=False):
        for q in final_state.get("sub_queries", []):
            st.markdown(f"- {q}")

    # Report
    st.subheader("Briefing Report")
    st.markdown(final_state.get("report", "No report generated."))

    st.divider()

    # Sources table
    with st.expander(f"All sources ({len(final_state.get('deduped', []))} articles)", expanded=False):
        for a in final_state.get("deduped", []):
            st.markdown(f"**{a.get('title', 'N/A')}**  \n{a.get('url', '')}")
            st.caption(f"Query: {a.get('query', '')}")
            st.markdown("---")
