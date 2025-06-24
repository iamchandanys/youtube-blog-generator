import os
import uvicorn

from fastapi import FastAPI, Request
from src.graphs.blog_graph_builder import BlogGraphBuilder
from src.llms.az_llm import AzLLM
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/generate-blog")
async def generate_blog(request: Request):
    try:
        data = await request.json()
        topic = data.get("topic", "")
        
        azLLm = AzLLM() 
        llm = azLLm.get_llm()
        
        blogGraphBuilder = BlogGraphBuilder(llm)
        graphBuilder = blogGraphBuilder.build_topic_graph()
        graph = graphBuilder.compile()
        state = graph.invoke({"topic": topic})
        
        return {"data": state}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)