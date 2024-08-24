import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.globals import set_debug, set_verbose

if os.environ.get("DEBUG", "0") == "1":
    set_debug(True)
    set_verbose(True)


model = ChatGoogleGenerativeAI(  # type: ignore
    max_output_tokens=1024,
    model="gemini-1.5-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY", ""),  # type: ignore
)

chain = (
    ChatPromptTemplate.from_messages([
        ("system", """\
Please extract and summarize the sections related to 'Termination Clauses' from the following terms and conditions document. Focus on the following details:

Conditions under which the agreement can be terminated by either party.
The process of termination, including any required notice periods.
Consequences of termination, such as loss of access to the software or data.
Any obligations that survive termination, such as confidentiality or payment obligations.
Ensure that the extracted information is clearly identified and easy to understand.
"""),
        ("user", "{text}"),
    ]) | model | StrOutputParser()
)
