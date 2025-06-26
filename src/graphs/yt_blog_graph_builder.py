from langgraph.graph import StateGraph, START, END
from src.states.yt_blog_state import YTBlogState
from src.nodes.yt_blog_node_definitions import YTBlogNodeDefinitions
from langchain_core.language_models.chat_models import BaseChatModel
from src.llms.az_llm import AzLLM

class YTBlogGraphBuilder:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.graph_builder = StateGraph(YTBlogState)
        
    def build_yt_blog_graph(self) -> StateGraph:
        # Add nodes to the graph
        self.graph_builder.add_node("transcription", YTBlogNodeDefinitions(self.llm).get_transcription_node)
        
        # Add edges to the graph
        self.graph_builder.add_edge(START, "transcription")
        self.graph_builder.add_edge("transcription", END)
        
        return self.graph_builder


# This code is for testing purposes in Langsmith
llm = AzLLM().get_llm()
yTBlogGraphBuilder = YTBlogGraphBuilder(llm)
graph = yTBlogGraphBuilder.build_yt_blog_graph().compile()

# https://www.youtube.com/watch?v=7onC2-SoHbc