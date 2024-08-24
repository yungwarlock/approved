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
Please identify and extract the section that specifies the governing law and jurisdiction applicable to this terms and conditions document.
The section should include details about the legal jurisdiction under which disputes will be resolved and the country or state laws that will govern the agreement.
"""),
        ("user", "{text}"),
    ]) | model | StrOutputParser()
)
