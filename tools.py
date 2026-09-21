from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

from rich import print

tavily= TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information.

    Args:
        query: The search query to use when searching the web.
    """
    results = tavily.search(
        query=query,
        max_results=5
    )

    out = []

    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)


@tool
def web_scrape(url: str) -> str:
    """Scrape a webpage and return its text.

    Args:
        url: The complete URL of the webpage to scrape.
    """
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(
            separator=" ",
            strip=True
        )[:3000]

    except Exception as e:
        return f"Could not scrape the URL: {str(e)}"

