import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# .env file se keys load karne ke liye
load_dotenv()

class BaseAgent:
    def __init__(self):
        # Ab yeh automatic aapki .env file se key uthayega, direct code mein kuch nahi hai
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=api_key)