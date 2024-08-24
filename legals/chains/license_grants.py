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
Please identify and extract the section(s) of this terms and conditions document that detail the License Grant. Focus on the following aspects:

The specific rights being granted to the user (e.g., personal use, commercial use, redistribution).
Any limitations or conditions attached to the license (e.g., non-transferable, non-exclusive).
The duration of the license (e.g., perpetual, time-limited).
Any geographical restrictions on the use of the software.
Provide the extracted text along with a brief summary highlighting the key points.
"""),
        ("user", "{text}"),
    ]) | model | StrOutputParser()
)
