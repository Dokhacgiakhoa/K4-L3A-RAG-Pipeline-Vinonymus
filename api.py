"""
FastAPI Server phục vụ giao diện Next.js PWA Chatbot và Slide Demo.
Endpoints:
  - POST /api/chat: Sinh câu trả lời kèm trích dẫn (citations) từ pipeline RAG Task 10.
  - POST /api/retrieve: Truy xuất chunks và scores từ pipeline Task 9 (hỗ trợ A/B test).
  - GET /api/health: Kiểm tra trạng thái hệ thống.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.task10_generation import generate_with_citation
from src.task9_retrieval_pipeline import retrieve

app = FastAPI(title="VinUni AI in Action RAG API", version="1.0.0")

# Cấu hình CORS cho Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5
    use_reranking: bool = True


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "VinUni AI in Action RAG Pipeline"}


@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        result = generate_with_citation(req.query, top_k=req.top_k)
        return result
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@app.post("/api/retrieve")
def retrieve_endpoint(req: RetrieveRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        results = retrieve(req.query, top_k=req.top_k, use_reranking=req.use_reranking)
        return {"results": results, "count": len(results)}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
