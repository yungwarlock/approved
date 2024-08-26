import re
import os
import json

import wikipedia
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain.globals import set_debug, set_verbose

if os.environ.get("DEBUG", "0") == "1":
    set_debug(True)
    set_verbose(True)


model = ChatGoogleGenerativeAI(  # type: ignore
    max_output_tokens=1024,
    model="gemini-1.5-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY", ""),  # type: ignore
)


def extract_text(text):
    return json.loads(re.search(r"(?<=```json)([\s\S]*?)(?=```)", text).group(1))[0]


def search(company):
    company_info = wikipedia.search(company)
    return company_info


def find_company_info(company):
    company_info = wikipedia.summary(company, auto_suggest=False)
    return company_info


chain = (
    {"result": RunnableLambda(search),
     "company": RunnablePassthrough()}
    | ChatPromptTemplate.from_messages([
        ("system", """\
The following is a result from a wikipedia search, which one of item is likely to be a history of {company} company
Output in JSON array
"""),
        ("user", "{result}"),
    ]) | model | StrOutputParser() | extract_text
    | RunnableLambda(find_company_info) | StrOutputParser()

    | ChatPromptTemplate.from_messages([
        ("system", """\
Your task is to extract the following information from this text:
- name: name of company
- about: a long summary of the company talking about: what they do, their products, market share and total users
- date_founded: the date it was founded
- location: location of it's headquarters
- website: their main website url
"""),
        ("user", "{text}"),
    ]) | model | StrOutputParser()
)
