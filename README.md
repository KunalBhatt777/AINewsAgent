# AI News Briefing Agent

An intelligent news research agent built with **LangGraph**, **LangChain**, **Claude Haiku 4.5** (via AWS Bedrock), and **Tavily Search**. Given any topic, it autonomously plans search queries, fetches articles, deduplicates results, and writes a structured news briefing — available as both a CLI tool and a Streamlit web UI.

---

## Demo

Enter a topic like `generative AI in healthcare 2025` and the agent produces:

- **Executive Summary** — 2-3 sentence overview
- **Key Developments** — bullet-pointed findings
- **Notable Sources** — titles with links

---

## Architecture

```
User Input (topic)
       │
       ▼
┌─────────────────────────────────────────────────┐
│              LangGraph StateGraph               │
│                                                 │
│  ┌──────────┐    ┌────────┐    ┌──────────┐    │
│  │ planner  │───▶│ search │───▶│  dedup   │    │
│  │  node    │    │  node  │    │   node   │    │
│  └──────────┘    └────────┘    └──────────┘    │
│       │               │              │          │
│  LLM generates   Tavily API     Remove dup     │
│  4 sub-queries   fetches news    URLs           │
│                                       │          │
│                               ┌───────▼──────┐  │
│                               │ report node  │  │
│                               │ LLM writes   │  │
│                               │ briefing     │  │
│                               └──────────────┘  │
└─────────────────────────────────────────────────┘
       │
       ▼
  Markdown Report
```

Each LLM node uses **LCEL runnables**:
```
ChatPromptTemplate  |  Claude Haiku 4.5  |  StrOutputParser
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent framework | LangGraph |
| LLM orchestration | LangChain (LCEL runnables) |
| LLM | Claude Haiku 4.5 via AWS Bedrock |
| Search | Tavily Search API |
| UI | Streamlit |

---

## Project Structure

```
AINewsAgent/
├── state.py          # AgentState TypedDict shared across all nodes
├── llm.py            # ChatBedrock client (Claude Haiku 4.5)
├── tools.py          # Tavily search wrapper
├── nodes.py          # Planner, search, dedup, report nodes (LCEL chains)
├── agent.py          # LangGraph StateGraph wiring all nodes
├── main.py           # CLI entry point
├── streamlit_app.py  # Streamlit web UI
└── requirements.txt
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/KunalBhatt777/AINewsAgent.git
cd AINewsAgent
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
```env
TAVILY_API_KEY=your_tavily_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-2
```

> **AWS setup:** You need an AWS account with Amazon Bedrock access and the Claude Haiku 4.5 model enabled. The first time you use an Anthropic model on Bedrock, you'll be prompted to fill out a short use case form.

> **Tavily API key:** Get a free key at [tavily.com](https://tavily.com).

---

## Usage

### Streamlit UI (recommended)
```bash
streamlit run streamlit_app.py
```
Opens at `http://localhost:8501` — enter any topic and click **Generate Briefing**.

### CLI
```bash
python main.py
```
Runs with the default topic. Edit the topic at the bottom of `main.py`.

---

## How It Works

1. **Planner node** — sends the topic to Claude with a system prompt instructing it to generate 4 targeted search queries
2. **Search node** — runs each query through Tavily Search (up to 5 results each, ~20 raw articles)
3. **Dedup node** — removes articles with duplicate URLs
4. **Report node** — sends all unique articles to Claude with a system prompt to write a structured briefing

State is passed between nodes via `AgentState` (a TypedDict), and each LLM call is a composable LCEL chain:

```python
chain = ChatPromptTemplate.from_messages([
    ("system", "..."),
    ("human", "{topic}"),
]) | llm | StrOutputParser()
```

---

## License

MIT
