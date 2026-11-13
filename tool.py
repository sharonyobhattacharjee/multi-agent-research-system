
import os
import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from tavily import TavilyClient
from langchain.tools import tool


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. Please check your .env file."
    )

# Initialize Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)


# --------------------------------------------------
# TOOL 1: WEB SEARCH
# --------------------------------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information
    about a given research topic.

    Returns source titles, URLs and search snippets.
    """

    if not query or not query.strip():
        return "Error: Search query cannot be empty."

    try:
        results = tavily.search(
            query=query.strip(),
            max_results=5,
            search_depth="advanced"
        )

        search_results = results.get("results", [])

        if not search_results:
            return "No relevant search results were found."

        output = []

        for index, result in enumerate(search_results, start=1):

            title = result.get("title", "No title available")
            url = result.get("url", "No URL available")
            content = result.get("content", "No snippet available")

            output.append(
                f"""
SOURCE {index}
Title: {title}
URL: {url}
Snippet: {content[:500]}
""".strip()
            )

        return "\n\n------------------------------\n\n".join(output)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# --------------------------------------------------
# TOOL 2: WEBPAGE SCRAPER
# --------------------------------------------------

@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage using its URL.

    Extracts readable webpage text and removes unnecessary
    HTML elements such as scripts, navigation and footers.
    """

    if not url or not url.strip():
        return "Error: URL cannot be empty."

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        return "Error: Please provide a valid HTTP or HTTPS URL."

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unnecessary HTML elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript"
        ]):
            tag.decompose()

        # Extract webpage title
        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "Untitled webpage"
        )

        # Extract readable text
        page_text = soup.get_text(
            separator="\n",
            strip=True
        )

        if not page_text:
            return f"No readable content found at: {url}"

        # Limit extracted content to avoid excessive token usage
        page_text = page_text[:6000]

        return (
            f"WEBPAGE TITLE: {title}\n"
            f"URL: {url}\n\n"
            f"WEBPAGE CONTENT:\n{page_text}"
        )

    except requests.exceptions.Timeout:
        return f"Error: The webpage timed out: {url}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP error while scraping {url}: {str(e)}"

    except requests.exceptions.RequestException as e:
        return f"Request failed for {url}: {str(e)}"

    except Exception as e:
        return f"Unexpected scraping error: {str(e)}"
