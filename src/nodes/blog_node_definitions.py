from src.states.blog_state import BlogState
from langchain_core.messages import HumanMessage
from src.states.blog_state import Blog
from langchain_core.language_models.chat_models import BaseChatModel

class BlogNodeDefinitions:
    """
    This class defines the node definitions for the blog application.
    It includes the node definitions for title creation and content generation
    """

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    def title_creation_node(self, state: BlogState) -> dict:
        """
        Node for creating the title of the blog post.
        """
        
        if "topic" in state and state["topic"]:
            system_message = f"You are an expert blog writer. Create a catchy title for a blog post about {state['topic']}."
            
            response = self.llm.invoke(system_message)
            
            return {
                "blog": {
                    "title": response.content,
                }
            }
            
    def content_generation_node(self, state: BlogState) -> dict:
        """
        Node for generating the content of the blog post.
        """
        
        if "blog" in state and "title" in state["blog"]:
            system_message = f"You are an expert blog writer. Write a detailed blog post about {state['topic']}."
            
            response = self.llm.invoke(system_message)
            
            return {
                "blog": {
                    "title": state["blog"]["title"],
                    "content": response.content,
                }
            }
            
    def translation_node(self, state: BlogState):
        """
        Node for translating the blog content to a specified language.
        This is a generic node that can be used for different languages.
        """
        
        if "blog" in state and "content" in state["blog"]:
            messages = [
                HumanMessage(
                    content = f"Translate the following blog content to {state['current_language']}: {state['blog']['content']}"
                )
            ]
            
            response = self.llm.with_structured_output(Blog).invoke(messages)
            
            return {
                **state,
                "blog": {
                    "title": response.title,
                    "content": response.content
                }
            }
            
    def route_node(self, state: BlogState):
        """
        Node for routing the blog content to the appropriate translation node based on the current language.
        """
        
        return {
            "topic": state["topic"],
            "current_language": state["current_language"]
        }
        
    def route_decision_node(self, state: BlogState):
        """
        Node for making a decision based on the current language.
        """
        
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "kannada":
            return "kannada"
        else:
            return state["current_language"]