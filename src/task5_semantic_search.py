"""
Task 5 — Semantic search.

Embed query bằng chính hàm của Task 4, query ChromaDB và đổi cosine distance
thành similarity. Output phải theo SearchResult, sort giảm dần và không quá top_k.
"""

from .task4_chunking_indexing import embed_texts, get_collection


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về dense SearchResult theo score giảm dần."""
    if not query.strip():
        return []

    query_vectors = embed_texts([query])
    if not query_vectors:
        return []

    collection = get_collection()
    response = collection.query(
        query_embeddings=query_vectors,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    ids = response["ids"][0] if response["ids"] else []
    documents = response["documents"][0] if response["documents"] else []
    metadatas = response["metadatas"][0] if response["metadatas"] else []
    distances = response["distances"][0] if response["distances"] else []

    results = []
    for item_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
        # Cosine distance trong ChromaDB: distance = 1 - cosine_similarity
        score = max(0.0, float(1.0 - distance))
        
        # Phục hồi url None nếu rỗng
        clean_meta = dict(metadata)
        if clean_meta.get("url") == "":
            clean_meta["url"] = None

        results.append({
            "id": item_id,
            "content": content,
            "score": round(score, 6),
            "metadata": clean_meta,
            "retrieval_method": "dense",
        })

    # Sắp xếp giảm dần theo điểm tương đồng và lấy đúng top_k
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for result in semantic_search("quy chế tuyển sinh học bổng", top_k=3):
        print(result)
