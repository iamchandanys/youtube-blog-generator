from langgraph.graph import StateGraph, START, END
from src.llms.az_llm import AzLLM

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph()