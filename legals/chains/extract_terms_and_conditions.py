import os
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.tools import tool
from langchain.globals import set_debug, set_verbose


if os.environ.get("DEBUG", "0") == "1":
    set_debug(True)
    set_verbose(True)


model = ChatGoogleGenerativeAI(  # type: ignore
    max_output_tokens=1024,
    model="gemini-1.5-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY", ""),  # type: ignore
)


def fetch_url(url: str) -> str:
    """Fetch the content of a URL."""

    url = f"https://r.jina.ai/{url}"
    headers = {
        # "Authorization": f"Bearer jina_f5e91efde1404c22a5b737a40ed34650bvV0QczVWAXpQzmsFGNSksNkfX8r"
    }

    try:
        # Fetch the content of the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""


@tool
def get_links(link: str) -> List[str]:
    """Get all the links from a given URL."""

    try:
        # Fetch the content of the page
        response = requests.get(link)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the anchor tags with href attributes
        links = [a['href'] for a in soup.find_all('a', href=True)]

        return links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []


tools = [TavilySearchResults(max_results=3), get_links]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
You are a tool to find the terms and conditions link in a page.
You will be given an initial link. From that link you can navigate and find other links using the `get_links` tool.
Output the link that is most probably leads to the terms and conditions page.
"""
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# Construct the Tools agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True)  # type: ignore

chain = (
    agent_executor

    | ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Output the url of the terms and conditions page from the given text. Remove any unwanted characters"
            ),
            ("human", "{output}"),
        ]
    ) | model | StrOutputParser()
)
