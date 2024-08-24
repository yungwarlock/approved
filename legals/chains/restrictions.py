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
Please identify and list all the restrictions outlined in the following terms and conditions document. Specifically, focus on any prohibitions related to:

Modifying, copying, or redistributing the software.
Reverse engineering or decompiling the software.
Unauthorized commercial use or sublicensing.
Sharing or transferring the software to third parties.
Use of the software in illegal or unethical activities.
Any other specific limitations on usage that are mentioned.
Ensure that all relevant sections and clauses that impose restrictions on the user's rights are clearly highlighted and summarized.
"""),
        ("user", "{text}"),
    ]) | model | StrOutputParser()
)
