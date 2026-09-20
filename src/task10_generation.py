"""
Task 10 — Generation có citation.

1. Retrieve top-k chunks từ pipeline Task 9.
2. Reorder để giảm lost-in-the-middle.
3. Format context kèm title và source.
4. Gọi LLM (Google Gemini / OpenAI / Anthropic).
5. Trả về answer, sources và retrieval_source theo GenerationResult contract.
"""

import os
from dotenv import load_dotenv
from .task9_retrieval_pipeline import retrieve

load_dotenv()

TOP_K = 5
TOP_P = 0.9
TEMPERATURE = 0.3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")

SYSTEM_PROMPT = """Bạn là Trợ lý AI chuyên trách tư vấn và giải đáp thông tin về "Chương trình Đào tạo Nhân tài AI Thực chiến" của Tập đoàn Vingroup và Trường Đại học VinUni (AI in Action).

Quy tắc bắt buộc:
1. Trả lời CHÍNH XÁC dựa trên ngữ cảnh (Context) được cung cấp dưới đây.
2. Với mỗi thông tin hoặc khẳng định quan trọng, hãy trích dẫn số thứ tự tài liệu nguồn tương ứng dạng [1], [2],...
3. Tuyệt đối không bịa đặt hoặc suy diễn thông tin nằm ngoài ngữ cảnh.
4. Nếu ngữ cảnh không có đủ thông tin hoặc câu hỏi hoàn toàn ngoài phạm vi chương trình, hãy từ chối lịch sự và nêu rõ: "Tôi không thể xác minh thông tin này từ nguồn hiện có."
5. Giọng văn chuyên nghiệp, nhiệt tình, chuẩn xác và dễ hiểu."""


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """Đưa chunks quan trọng về đầu và cuối context (Lost in the Middle)."""
    if len(chunks) <= 2:
        return list(chunks)
    front = chunks[::2]
    back = chunks[1::2]
    return list(front + back[::-1])


def format_context(chunks: list[dict]) -> str:
    """Tạo context có title và source label rõ ràng cho LLM trích dẫn."""
    parts = []
    for index, chunk in enumerate(chunks, 1):
        metadata = chunk["metadata"]
        title = metadata.get("title", "Tài liệu")
        source = metadata.get("source", "Tài liệu gốc")
        content = chunk.get("content", "").strip()
        parts.append(
            f"--- [Tài liệu {index} | Title: {title} | Source: {source}] ---\n{content}"
        )
    return "\n\n".join(parts)


def call_llm(system_prompt: str, user_message: str) -> str:
    """Gọi LLM theo cấu hình provider trong .env (ưu tiên Google Gemini)."""
    provider = os.getenv("LLM_PROVIDER", LLM_PROVIDER).lower()
    model_name = os.getenv("LLM_MODEL", LLM_MODEL)

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình trong .env")
        from google import genai
        client = genai.Client(api_key=api_key)
        full_prompt = f"{system_prompt}\n\n{user_message}"
        response = client.models.generate_content(
            model=model_name or "gemini-3.6-flash",
            contents=full_prompt,
        )
        return response.text.strip() if response.text else "Không nhận được phản hồi từ mô hình."

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=model_name or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=TEMPERATURE,
        )
        return completion.choices[0].message.content.strip()

    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model_name or "claude-3-5-haiku-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text.strip()

    else:
        raise ValueError(f"Provider không hỗ trợ: {provider}")


def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """Trả về GenerationResult chuẩn hợp đồng."""
    if not query.strip():
        return {
            "answer": "Vui lòng nhập câu hỏi cần tra cứu.",
            "sources": [],
            "retrieval_source": "none",
        }

    chunks = retrieve(query, top_k=top_k)
    if not chunks:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": [],
            "retrieval_source": "none",
        }

    reordered = reorder_for_llm(chunks)
    context = format_context(reordered)
    user_message = f"Câu hỏi của học viên: {query}\n\nNgữ cảnh tham chiếu:\n{context}"

    try:
        answer = call_llm(SYSTEM_PROMPT, user_message)
    except Exception as err:
        print(f"[WARN] Lỗi khi gọi LLM: {err}")
        answer = "Tôi không thể xác minh thông tin này từ nguồn hiện có."
        return {
            "answer": answer,
            "sources": [],
            "retrieval_source": "none",
        }

    retrieval_source = chunks[0]["retrieval_method"] if chunks else "none"

    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": retrieval_source,
    }


if __name__ == "__main__":
    test_q = "Chương trình AI Thực chiến có học bổng thế nào?"
    print(f"Query: {test_q}")
    result = generate_with_citation(test_q, top_k=3)
    print("\n--- Answer ---")
    print(result["answer"])
    print(f"\n--- Sources ({len(result['sources'])}) ---")
    for s in result["sources"]:
        print(f"- [{s['retrieval_method']}] {s['metadata']['title']} (Score: {s['score']})")
