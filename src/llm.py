from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

model = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPEN_AI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)