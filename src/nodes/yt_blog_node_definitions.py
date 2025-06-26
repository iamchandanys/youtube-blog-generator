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