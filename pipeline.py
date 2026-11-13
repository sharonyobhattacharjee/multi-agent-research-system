
from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:
    """
    Runs the complete multi-agent research workflow:

    1. Search Agent  - Finds relevant web sources.
    2. Reader Agent  - Scrapes relevant webpages.
    3. Writer Agent  - Generates a structured research report.
    4. Critic Agent  - Evaluates the generated report.
    """

    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    topic = topic.strip()

    state = {
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": ""
    }

    # --------------------------------------------------
    # STEP 1: SEARCH AGENT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 1: SEARCH AGENT IS WORKING...")
    print("=" * 60)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Find recent, reliable and relevant information "
                    f"about the following research topic: {topic}. "
                    "Use the web search tool and provide the source "
                    "titles, URLs and useful findings."
                )
            }
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSEARCH RESULTS:\n")
    print(state["search_results"])

    # --------------------------------------------------
    # STEP 2: READER AGENT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 2: READER AGENT IS WORKING...")
    print("=" * 60)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Research topic: {topic}\n\n"
                    "Read the search results below. Identify the "
                    "most relevant URLs and use the webpage scraping "
                    "tool to extract their content.\n\n"
                    "Prioritize reliable and authoritative sources. "
                    "Scrape multiple relevant URLs when possible. "
                    "Do not invent webpage content.\n\n"
                    f"SEARCH RESULTS:\n{state['search_results'][:6000]}"
                )
            }
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nSCRAPED CONTENT:\n")
    print(state["scraped_content"])

    # --------------------------------------------------
    # STEP 3: WRITER AGENT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 3: WRITER AGENT IS WORKING...")
    print("=" * 60)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    state["report"] = report

    print("\nGENERATED RESEARCH REPORT:\n")
    print(state["report"])

    # --------------------------------------------------
    # STEP 4: CRITIC AGENT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 4: CRITIC AGENT IS WORKING...")
    print("=" * 60)

    feedback = critic_chain.invoke({
        "report": state["report"]
    })

    state["feedback"] = feedback

    print("\nCRITIC FEEDBACK:\n")
    print(state["feedback"])

    # --------------------------------------------------
    # PIPELINE COMPLETED
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("RESEARCH PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    return state


# --------------------------------------------------
# RUN PIPELINE DIRECTLY
# --------------------------------------------------

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ").strip()

    try:
        result = run_research_pipeline(topic)

    except Exception as error:
        print("\nPIPELINE FAILED!")
        print(f"Error: {error}")
