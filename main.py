from dotenv import load_dotenv
load_dotenv()

from agent import app


def run_briefing(topic: str):
    print(f"\n{'='*60}")
    print(f"AI News Briefing Agent")
    print(f"Topic: {topic}")
    print(f"{'='*60}\n")

    state = app.invoke({"topic": topic})

    print("Sub-queries generated:")
    for q in state["sub_queries"]:
        print(f"  - {q}")

    print(f"\nArticles found (after dedup): {len(state['deduped'])}")
    print(f"\n{'='*60}")
    print("BRIEFING REPORT")
    print(f"{'='*60}\n")
    print(state["report"])
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    run_briefing("generative AI in healthcare 2025")
