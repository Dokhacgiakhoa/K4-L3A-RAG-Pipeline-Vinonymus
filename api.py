"""
FastAPI Server phục vụ giao diện Next.js PWA Chatbot và Slide Demo.
Endpoints:
  - POST /api/chat: Sinh câu trả lời kèm trích dẫn (citations) từ pipeline RAG Task 10.
  - POST /api/retrieve: Truy xuất chunks và scores từ pipeline Task 9 (hỗ trợ A/B test).
  - POST /api/pipeline_trace: Truy vết chi tiết từng bước từ input -> parallel search -> RRF -> fallback check -> reorder -> generation.
  - GET /api/health: Kiểm tra trạng thái hệ thống.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.task10_generation import generate_with_citation, reorder_for_llm
from src.task9_retrieval_pipeline import retrieve, SCORE_THRESHOLD
from src.task5_semantic_search import semantic_search
from src.task6_lexical_search import lexical_search
from src.task7_reranking import rerank_rrf

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="VinUni AI in Action RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SLIDES_DIR = Path(__file__).resolve().parent / "slides"
if SLIDES_DIR.exists():
    app.mount("/slides", StaticFiles(directory=str(SLIDES_DIR)), name="slides")

@app.get("/")
def index_redirect():
    index_file = SLIDES_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "VinUni AI in Action RAG API is running."}


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


@app.post("/api/pipeline_trace")
def pipeline_trace_endpoint(req: ChatRequest):
    """Truy vết chi tiết luồng AI từng bước phục vụ màn hình demo 2 cột."""
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Bước 1: Phân tích Input Query
        step1_input = {
            "raw_query": q,
            "char_count": len(q),
            "word_count": len(q.split()),
        }

        # Bước 2: Song song Dense Semantic & Sparse BM25
        dense_results = semantic_search(q, top_k=req.top_k)
        sparse_results = lexical_search(q, top_k=req.top_k)

        # Bước 3: RRF Reranking
        fused_results = rerank_rrf([dense_results, sparse_results], top_k=req.top_k)

        # Bước 4: Kiểm tra Cosine Threshold & Quyết định Fallback
        best_dense_score = dense_results[0]["score"] if dense_results else 0.0
        fallback_triggered = best_dense_score < SCORE_THRESHOLD
        threshold_decision = {
            "best_dense_score": best_dense_score,
            "score_threshold": SCORE_THRESHOLD,
            "fallback_triggered": fallback_triggered,
            "selected_strategy": "fallback_pageindex" if fallback_triggered else "hybrid_rrf",
        }

        # Bước 5: Lost-in-the-middle Context Reordering
        effective_chunks = retrieve(q, top_k=req.top_k)
        reordered_chunks = reorder_for_llm(effective_chunks) if effective_chunks else []

        # Bước 6: Sinh phản hồi có Citation từ LLM (Gemini)
        gen_result = generate_with_citation(q, top_k=req.top_k)

        return {
            "query": q,
            "step_1_input": step1_input,
            "step_2_dense": dense_results,
            "step_2_sparse": sparse_results,
            "step_3_rrf": fused_results,
            "step_4_threshold": threshold_decision,
            "step_5_reordered": reordered_chunks,
            "step_6_generation": gen_result,
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
