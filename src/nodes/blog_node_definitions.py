from src.states.blog_state import BlogState

class BlogNodeDefinitions:
    """
    This class defines the node definitions for the blog application.
    It includes the node definitions for title creation and content generation
    """

    def __init__(self, llm):
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
        
        