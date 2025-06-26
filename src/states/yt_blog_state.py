from typing import TypedDict
from pydantic import BaseModel, Field

class YTBlog(BaseModel):
    title: str = Field(description="The title of the blog post")
    content: str = Field(description="The content of the blog post")
    
class YTBlogState(TypedDict):
    messages: str
    transcript: str
    blog: YTBlog
    current_language: str