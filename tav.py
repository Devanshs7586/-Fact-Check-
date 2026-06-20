import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = st.secrets.get(
    "TAVILY_API_KEY",
    os.getenv("TAVILY_API_KEY")
)

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_evidence(claim: str):
    try:
        response = tavily_client.search(
            query=claim,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )

        results = response.get("results", [])
        answer = response.get("answer", "")

        evidence_text = ""

        if answer:
            evidence_text += f"Tavily Answer:\n{answer}\n\n"

        for idx, item in enumerate(results, start=1):
            title = item.get("title", "")
            url = item.get("url", "")
            content = item.get("content", "")

            evidence_text += f"Source {idx}:\n"
            evidence_text += f"Title: {title}\n"
            evidence_text += f"URL: {url}\n"
            evidence_text += f"Content: {content}\n\n"

        return evidence_text, results

    except Exception as e:
        return f"Search error: {str(e)}", []