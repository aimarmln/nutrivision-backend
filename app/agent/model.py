from langchain_groq import ChatGroq
from app.config import Config

model = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=Config.GROQ_API_KEY,
    temperature=0.3,
    reasoning_effort="low",
    max_tokens=500,
)
