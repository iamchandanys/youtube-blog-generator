import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

class AzLLM:
    def __init__(self):
        load_dotenv()
        
    def get_llm(self) -> any:
        try:
            llm = init_chat_model("azure_openai:gpt-4o-mini")
            return llm
        except Exception as e:
            raise Exception(f"Failed to initialize Azure LLM: {e}")