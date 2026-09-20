"""
Task 9 — Retrieval pipeline hoàn chỉnh.

Luồng xử lý:
    1. Chạy semantic_search và lexical_search.
    2. Kiểm tra best cosine score gốc từ dense results.
    3. Nếu best_dense_score < score_threshold: Thử PageIndex fallback.
    4. Nếu fallback thành công: Trả về kết quả pageindex.
    5. Nếu best_dense_score >= score_threshold hoặc fallback lỗi/rỗng:
       Fuse dense và sparse bằng RRF đúng một lần.
"""

from .task5_semantic_search import semantic_search
from .task6_lexical_search import lexical_search
from .task7_reranking import rerank_rrf
from .task8_pageindex_vectorless import pageindex_search


SCORE_THRESHOLD = 0.35
DEFAULT_TOP_K = 5


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """Trả về hybrid hoặc pageindex SearchResult theo contract."""
    dense = semantic_search(query, top_k=top_k)
    sparse = lexical_search(query, top_k=top_k)

    best_dense_score = dense[0]["score"] if dense else 0.0

    # Nếu dense score dưới ngưỡng, kích hoạt fallback
    if best_dense_score < score_threshold:
        try:
            fallback = pageindex_search(query, top_k=top_k)
            if fallback:
                return fallback
        except Exception:
            # Fallback service lỗi -> tiếp tục trả về hybrid/dense
            pass

    # Nếu tự tin hoặc fallback không khả dụng -> gộp thứ hạng qua RRF
    if use_reranking:
        hybrid = rerank_rrf([dense, sparse], top_k=top_k)
        return hybrid

    return dense[:top_k]


if __name__ == "__main__":
    res = retrieve("tuyển sinh khóa 4 AI thực chiến", top_k=3)
    for item in res:
        print(f"[{item['retrieval_method']}] score={item['score']} - {item['metadata']['title']}")
