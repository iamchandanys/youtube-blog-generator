from src.states.yt_blog_state import YTBlogState, YTBlog
from src.tools.transcript_tool import get_youtube_transcript
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from src.tools.transcript_tool import get_youtube_transcript

class YTBlogNodeDefinitions:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def get_transcription_node(self, state: YTBlogState):
        """
        Node to fetch the transcript of a YouTube video.
        """
        
        transcript = get_youtube_transcript(f"{state['messages']}")
        
        return {
            "transcript": "\n".join([message for message in transcript])
        }
        
    def get_title_and_content_node(self, state: YTBlogState):
        """
        Node to generate the title and content of the blog post based on the transcript.
        """
        
        transcript = state["transcript"]
        
        messages = [
            HumanMessage(
                content=f"Generate a catchy title and detailed content for a blog post based on the following YouTube video transcript: {transcript}"
            )
        ]
        
        response = self.llm.with_structured_output(YTBlog).invoke(messages)
        
        return {
            "blog": {
                "title": response.title,
                "content": response.content
            }
        }
        
    def translate_title_and_content_node(self, state: YTBlogState):
        """
        Node to translate the title and content of the blog post to a specified language.
        """
        
        if "blog" in state and "content" in state["blog"]:
            messages = [
                HumanMessage(
                    content=f"Translate the following blog content to {state['current_language']}: {state['blog']['content']}. Additionally, provide a catchy title for the blog post."
                )
            ]
            
            response = self.llm.with_structured_output(YTBlog).invoke(messages)
            
            return {
                "blog": {
                    "title": response.title,
                    "content": response.content
                }
            }