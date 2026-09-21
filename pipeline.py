from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state={}

    print("\n"+"="*50)
    print("step 1 search agent is working...   ")
    print("="*50+"\n")

    # Step 1: Web Search
    search_agent = build_search_agent()

    search_results = search_agent.invoke({
        "messages": [
            (
                "user",
                f"""Search for recent and reliable information about:

    {topic}

    Return only the most relevant results.
    For each result provide:
    - Title
    - URL
    - Short summary

    Keep the response concise."""
            )
        ]
    })

    state["search_results"] = search_results["messages"][-1].content

    print("\n search_results: ", state['search_results'])

    print("\n"+"="*50)
    print("step 2 scrape agent is working...   ")
    print("="*50+"\n")

    # Step 2: Web Scraping
    reader_agent = build_scrape_agent()

    reader_results = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""Based on the search results below, select the 2 most relevant URLs
    and scrape them for deeper information.

    Topic:
    {topic}

    Search Results:
    {state["search_results"][:3000]}

    Return only important factual information.
    Keep the response concise."""
            )
        ]
    })

    state["scrape_content"] = reader_results["messages"][-1].content

    print("\n scrape_content: ", state['scrape_content'])

    print("\n"+"="*50)
    print("step 3 writer chain is working...   ")
    print("="*50+"\n")

    #   Step 3: writer chain

    research_combined=(
        f"Search Results:\n{state['search_results']}\n\n"
        f"Scraped Content:\n{state['scrape_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print(f"\n Final Research Report:\n{state['report']}")

    print("\n"+"="*50)
    print("step 4 critic prompt is working...   ")
    print("="*50+"\n")

    #step 4: Critic Report

    state['feedback'] = critic_chain.invoke({
        "report": state['report']
    })

    print(f"\n Critic Report:\n{state['feedback']}")

    return state


if __name__ == "__main__":
    topic = input("Enter the research topic: ")
    run_research_pipeline(topic)
