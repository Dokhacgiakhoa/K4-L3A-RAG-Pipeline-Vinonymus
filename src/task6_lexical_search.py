"""
Task 6 — Lexical search bằng BM25 (chuẩn Lucene BM25).

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""

import math
import numpy as np


CORPUS: list[dict] = []
_bm25_instance = None
_cached_corpus_len = 0


class RobustBM25:
    """Hiện thực BM25 chuẩn Lucene/Elasticsearch để tránh trường hợp IDF = 0 khi corpus nhỏ."""

    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.corpus_size = len(corpus)
        self.avgdl = (
            sum(len(doc) for doc in corpus) / self.corpus_size
            if self.corpus_size > 0
            else 1.0
        )
        self.k1 = k1
        self.b = b
        self.idf: dict[str, float] = {}

        for doc in corpus:
            for word in set(doc):
                self.idf[word] = self.idf.get(word, 0) + 1

        # Lucene IDF formula: log(1 + (N - n + 0.5) / (n + 0.5))
        for word, freq in self.idf.items():
            self.idf[word] = math.log(1.0 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def get_scores(self, query: list[str]) -> list[float]:
        scores = []
        for doc in self.corpus:
            score = 0.0
            doc_len = len(doc)
            for word in query:
                if word in self.idf:
                    tf = doc.count(word)
                    if tf > 0:
                        denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                        score += self.idf[word] * (tf * (self.k1 + 1.0)) / denominator
            scores.append(score)
        return scores


def _ensure_corpus():
    """Tự động nạp corpus nếu danh sách CORPUS đang rỗng."""
    global CORPUS
    if not CORPUS:
        try:
            from .task4_chunking_indexing import chunk_documents, load_documents
            CORPUS = chunk_documents(load_documents())
        except Exception:
            CORPUS = []


def build_bm25_index(corpus: list[dict]):
    """Tạo BM25 index từ cùng corpus chunks của Task 4."""
    if not corpus:
        return None
    tokenized = [item["content"].lower().split() for item in corpus]
    return RobustBM25(tokenized)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    global _bm25_instance, _cached_corpus_len
    _ensure_corpus()

    if not CORPUS or not query.strip():
        return []

    if _bm25_instance is None or len(CORPUS) != _cached_corpus_len:
        _bm25_instance = build_bm25_index(CORPUS)
        _cached_corpus_len = len(CORPUS)

    if _bm25_instance is None:
        return []

    query_tokens = query.lower().split()
    if not query_tokens:
        return []

    scores = _bm25_instance.get_scores(query_tokens)
    indices = np.argsort(scores)[::-1]

    results = []
    seen_ids = set()

    for index in indices:
        item = CORPUS[index]
        item_id = item["id"]
        if item_id in seen_ids:
            continue

        score = float(scores[index])
        clean_meta = dict(item["metadata"])
        if clean_meta.get("url") == "":
            clean_meta["url"] = None

        results.append({
            "id": item_id,
            "content": item["content"],
            "score": round(score, 6),
            "metadata": clean_meta,
            "retrieval_method": "bm25",
        })
        seen_ids.add(item_id)

        if len(results) >= top_k:
            break

    # Đảm bảo sắp xếp giảm dần theo điểm số
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for result in lexical_search("học bổng trợ cấp 8 triệu", top_k=3):
        print(result)
