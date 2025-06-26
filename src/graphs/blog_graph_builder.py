from langgraph.graph import StateGraph, START, END
from src.states.blog_state import BlogState
from src.nodes.blog_node_definitions import BlogNodeDefinitions
from src.llms.az_llm import AzLLM

class BlogGraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = StateGraph(BlogState)
    
    def build_topic_graph(self) -> StateGraph:
        blog_node_definitions = BlogNodeDefinitions(self.llm)
        
        # Add nodes for topic generation
        # Passing a reference to the function (or callable) title_creation_node & content_generation_node, not calling it directly. 
        # The graph framework (StateGraph) is responsible for calling this function later, and when it does, 
        # it will pass the current state (an instance of BlogState) as an argument.
        self.graph_builder.add_node("title_creation", blog_node_definitions.title_creation_node)
        self.graph_builder.add_node("content_generation", blog_node_definitions.content_generation_node)
        
        # Add edges to connect the nodes
        self.graph_builder.add_edge(START, "title_creation")
        self.graph_builder.add_edge("title_creation", "content_generation")
        self.graph_builder.add_edge("content_generation", END)
        
        return self.graph_builder
    
    def build_topic_with_language_graph(self) -> StateGraph:
        blog_node_definitions = BlogNodeDefinitions(self.llm)
        
        self.graph_builder.add_node("title_creation", blog_node_definitions.title_creation_node)
        self.graph_builder.add_node("content_generation", blog_node_definitions.content_generation_node)
        self.graph_builder.add_node("route", blog_node_definitions.route_node)
        self.graph_builder.add_node("hindi_translation", lambda state: blog_node_definitions.translation_node({**state, "current_language": "hindi"}))
        self.graph_builder.add_node("kannada_translation", lambda state: blog_node_definitions.translation_node({**state, "current_language": "kannada"}))
        
        self.graph_builder.add_edge(START, "title_creation")
        self.graph_builder.add_edge("title_creation", "content_generation")
        self.graph_builder.add_edge("content_generation", "route")
        self.graph_builder.add_conditional_edges(
            "route",
            blog_node_definitions.route_decision_node,
            {
                "hindi": "hindi_translation",
                "kannada": "kannada_translation",
            }
        )
        self.graph_builder.add_edge("hindi_translation", END)
        self.graph_builder.add_edge("kannada_translation", END)
        
        return self.graph_builder
    
    def get_graph_builder(self, use_case: str):
        if(use_case == "topic_with_language"):
            self.build_topic_with_language_graph()
        if(use_case == "topic"):
            self.build_topic_graph()
            
        return self.graph_builder.compile()


# This code is for testing purposes in Langsmith
llm = AzLLM().get_llm()
blogGraphBuilder = BlogGraphBuilder(llm)
graph = blogGraphBuilder.build_topic_with_language_graph().compile()

response = graph.invoke(
    {
        "topic": "short note on AI",
    }
)