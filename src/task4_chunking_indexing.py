"""
Task 4 — Chunking, embedding và indexing.

1. Đọc toàn bộ Markdown trong data/standardized/ (cả legal và news).
2. Chia văn bản bằng RecursiveCharacterTextSplitter.
3. Embed chunks bằng sentence-transformers hoặc Gemini.
4. Upsert vào ChromaDB với cosine distance (hnsw:space = cosine).
"""

import os
from pathlib import Path
import re
from dotenv import load_dotenv
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
STANDARDIZED_DIR = ROOT_DIR / "data" / "standardized"
CHROMA_DIR = ROOT_DIR / "chroma_db"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "sentence_transformers")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = "rag_documents"

_embed_model = None


def get_embedding_model():
    """Khởi tạo mô hình sentence-transformers một lần (singleton)."""
    global _embed_model
    if _embed_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embed_model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception:
            from sentence_transformers import SentenceTransformer
            _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embed_model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Tạo vector embeddings cho danh sách văn bản."""
    if not texts:
        return []

    # Ưu tiên sentence_transformers local
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.tolist()


def get_collection():
    """Mở Chroma collection dùng cosine distance."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def load_documents() -> list[dict]:
    """Đọc Markdown trong data/standardized/ và trả về danh sách Document theo contract."""
    documents = []

    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        if not path.is_file():
            continue

        raw_content = path.read_text(encoding="utf-8").strip()
        if not raw_content:
            continue

        doc_type = "legal" if "legal" in path.parts else "news"
        doc_id = path.stem

        # Trích xuất title và URL nếu có trong header
        title_match = re.search(r"^#\s+(.+)$", raw_content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem.replace("-", " ").title()

        url_match = re.search(r"\*\*Source:\*\*\s*(https?://[^\s]+)", raw_content)
        url = url_match.group(1).strip() if url_match else None

        documents.append({
            "id": doc_id,
            "content": raw_content,
            "metadata": {
                "source": path.name,
                "title": title,
                "doc_type": doc_type,
                "url": url,
            },
        })

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chia Document thành chunks có id và chunk_index tuân thủ contract."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for document in documents:
        split_texts = splitter.split_text(document["content"])
        doc_id = document["id"]
        for index, text in enumerate(split_texts):
            clean_text = text.strip()
            if not clean_text:
                continue
            chunks.append({
                "id": f"{doc_id}-{index}",
                "content": clean_text,
                "metadata": {
                    "source": document["metadata"]["source"],
                    "title": document["metadata"]["title"],
                    "doc_type": document["metadata"]["doc_type"],
                    "url": document["metadata"].get("url"),
                    "chunk_index": index,
                },
            })

    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Thêm embedding vector vào từng chunk."""
    if not chunks:
        return []

    texts = [chunk["content"] for chunk in chunks]
    vectors = embed_texts(texts)

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector

    return chunks


def index_to_vectorstore(chunks: list[dict]) -> None:
    """Upsert chunks vào ChromaDB."""
    if not chunks:
        return

    collection = get_collection()

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    embeddings = [chunk["embedding"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    # ChromaDB không cho phép metadata có value None, chuyển None thành ""
    sanitized_metadatas = []
    for meta in metadatas:
        sanitized = {}
        for k, v in meta.items():
            sanitized[k] = "" if v is None else v
        sanitized_metadatas.append(sanitized)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=sanitized_metadatas,
    )


def run_pipeline() -> None:
    """Chạy load, chunk, embed và index."""
    documents = load_documents()
    print(f"Loaded {len(documents)} documents from {STANDARDIZED_DIR}")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    embedded_chunks = embed_chunks(chunks)
    print(f"Generated embeddings for {len(embedded_chunks)} chunks")

    index_to_vectorstore(embedded_chunks)
    print(f"Successfully indexed {len(embedded_chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    run_pipeline()
