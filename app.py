"""
Streamlit Application — Sổ Tay Nhân Tài AI Thực Chiến (Vingroup & VinUni).
Hiển thị câu trả lời có citation, nguồn trích dẫn và điểm độ tương đồng.
"""

import streamlit as st
from dotenv import load_dotenv
from src.task10_generation import generate_with_citation
from src.task9_retrieval_pipeline import retrieve

load_dotenv()

st.set_page_config(
    page_title="AI in Action — Sổ Tay AI Thực Chiến",
    page_icon="🤖",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚙️ Cấu hình RAG")
    st.caption("Chương trình Đào tạo Nhân tài AI Thực chiến — Vingroup & VinUni")
    top_k = st.slider("Số lượng Chunks (top_k)", 1, 10, 5)
    use_hybrid = st.toggle("Sử dụng Hybrid Search (RRF)", value=True)
    st.divider()
    st.markdown("""
    **Nguồn dữ liệu xác thực:**
    - 📄 *20K AI Handbook v2.1* (Cẩm nang VinUni)
    - 📄 *Quyết định 1290/QĐ-BKHCN* (Bộ KH&CN)
    - 📄 *AI Mentor Blueprint & Demo Slides*
    - 🌐 *Cổng thông tin tuyển sinh VinUni*
    """)
    if st.button("Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Trợ Lý Sổ Tay Nhân Tài AI Thực Chiến")
st.caption("Hỏi đáp thông tin tuyển sinh, học bổng 100%, trợ cấp 8 triệu/tháng, chuẩn SFIA và lộ trình 12 tuần thực chiến dự án Vingroup.")

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander(f"📚 Nguồn trích dẫn ({len(message['sources'])} tài liệu | {message.get('retrieval_source', 'hybrid')})"):
                for idx, src in enumerate(message["sources"], 1):
                    score_val = src.get("score", 0.0)
                    method = src.get("retrieval_method", "dense")
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{idx}] {meta.get('title', 'Tài liệu')}** `{meta.get('source', '')}` (Method: `{method}`, Score: `{score_val:.4f}`)")
                    st.caption(src.get("content", "")[:300] + "...")

query = st.chat_input("Hỏi về học bổng, quy trình thi tuyển, chuẩn SFIA, trợ cấp...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm tài liệu và sinh câu trả lời..."):
            result = generate_with_citation(query, top_k=top_k)
            answer = result["answer"]
            sources = result.get("sources", [])
            retrieval_source = result.get("retrieval_source", "none")

            st.markdown(answer)

            if sources:
                with st.expander(f"📚 Nguồn trích dẫn ({len(sources)} tài liệu | Phương pháp: {retrieval_source})"):
                    for idx, src in enumerate(sources, 1):
                        score_val = src.get("score", 0.0)
                        method = src.get("retrieval_method", "dense")
                        meta = src.get("metadata", {})
                        st.markdown(f"**[{idx}] {meta.get('title', 'Tài liệu')}** `{meta.get('source', '')}` (Method: `{method}`, Score: `{score_val:.4f}`)")
                        st.caption(src.get("content", "")[:300] + "...")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source,
    })
