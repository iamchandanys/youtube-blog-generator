import os
import uvicorn

from fastapi import FastAPI, Request
# from src.graphs.blog_graph_builder import BlogGraphBuilder
from src.graphs.yt_blog_graph_builder import YTBlogGraphBuilder
from src.llms.az_llm import AzLLM
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# @app.post("/generate-blog")
# async def generate_blog(request: Request):
#     try:
#         data = await request.json()
#         topic = data.get("topic", "")
#         language = data.get("language", "")
        
#         azLLm = AzLLM() 
#         llm = azLLm.get_llm()
        
#         blogGraphBuilder = BlogGraphBuilder(llm)
        
#         if topic and language:
#             graphBuilder = blogGraphBuilder.get_graph_builder("topic_with_language")
#             state = graphBuilder.invoke({"topic": topic, "current_language": language})
#         else:
#             graphBuilder = blogGraphBuilder.get_graph_builder("topic")
#             state = graphBuilder.invoke({"topic": topic})

#         return {"data": state}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
    
@app.post("/generate-yt-blog")
async def generate_yt_blog(request: Request):
    try:
        data = await request.json()
        user_message = data.get("user_message", "")
        
        azLLm = AzLLM() 
        llm = azLLm.get_llm()
        
        yTBlogGraphBuilder = YTBlogGraphBuilder(llm)
        
        graphBuilder = yTBlogGraphBuilder.build_yt_blog_graph()
        
        state = graphBuilder.compile().invoke(
            {
                "user_message": user_message,
            }
        )

        return {"data": state}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)