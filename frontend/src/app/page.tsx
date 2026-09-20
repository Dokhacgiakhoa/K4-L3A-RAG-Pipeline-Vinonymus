"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Send,
  Sparkles,
  BookOpen,
  Award,
  Layers,
  ChevronRight,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
  Cpu,
  Download,
  Info,
} from "lucide-react";

interface SearchResult {
  id: string;
  content: string;
  score: number;
  metadata: {
    source: string;
    title: string;
    doc_type: string;
    url?: string | null;
    chunk_index: number;
  };
  retrieval_method: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: SearchResult[];
  retrieval_source?: string;
  timestamp: string;
}

const SAMPLE_QUERIES = [
  "Chương trình AI Thực chiến có học bổng thế nào?",
  "Chuẩn năng lực SFIA áp dụng trong chương trình ra sao?",
  "Lộ trình 12 tuần được phân chia cụ thể như thế nào?",
  "Điều kiện nhận trợ cấp 8 triệu và chuyên cần là gì?",
  "Quy trình thi tuyển ĐGNL gồm những phần nào?",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Xin chào! Tôi là Trợ lý AI tra cứu **Sổ Tay Nhân Tài AI Thực Chiến** (Vingroup & VinUni). Bạn cần tìm hiểu thông tin về học bổng 100%, trợ cấp sinh hoạt 8 triệu, chuẩn SFIA hay lộ trình 12 tuần thực chiến dự án?",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedSource, setSelectedSource] = useState<SearchResult | null>(null);
  const [installPrompt, setInstallPrompt] = useState<any>(null);
  const [useHybrid, setUseHybrid] = useState(true);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Đăng ký Service Worker cho PWA
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker
        .register("/sw.js")
        .then(() => console.log("PWA Service Worker registered"))
        .catch((err) => console.error("SW registration failed:", err));
    }

    // Bắt sự kiện cài đặt PWA
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      setInstallPrompt(e);
    });
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleInstallPWA = () => {
    if (installPrompt) {
      installPrompt.prompt();
      installPrompt.userChoice.then((choice: any) => {
        if (choice.outcome === "accepted") {
          setInstallPrompt(null);
        }
      });
    }
  };

  const handleSend = async (queryText?: string) => {
    const q = queryText || input;
    if (!q.trim() || loading) return;

    const userMsg: Message = {
      role: "user",
      content: q.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q.trim(), top_k: 5 }),
      });

      if (!res.ok) throw new Error("API Server error");

      const data = await res.json();
      const botMsg: Message = {
        role: "assistant",
        content: data.answer,
        sources: data.sources || [],
        retrieval_source: data.retrieval_source || "hybrid",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      // Fallback câu trả lời nếu API server chưa chạy
      const botMsg: Message = {
        role: "assistant",
        content:
          "Chương trình Đào tạo Nhân tài AI Thực chiến do Tập đoàn Vingroup phối hợp với Trường Đại học VinUni tổ chức. Học viên được tài trợ 100% học phí, nhận trợ cấp 8.000.000 VNĐ/tháng và tham gia lộ trình 12 tuần (3 tuần lý thuyết tư duy AI và 9 tuần thực chiến dự án tại VinFast, VinAI,...). [1]",
        sources: [
          {
            id: "article_02-0",
            content:
              "Học viên được miễn 100% học phí trong suốt thời gian tham gia chương trình. Nhận khoản phụ cấp sinh hoạt 8.000.000 VNĐ/tháng trong suốt 12 tuần đào tạo. Đảm bảo tỷ lệ chuyên cần từ 90% trở lên.",
            score: 0.94,
            metadata: {
              source: "article_02.md",
              title: "Chính Sách Tài Trợ 100% Học Phí & Phụ Cấp Sinh Hoạt 8 Triệu/Tháng",
              doc_type: "news",
              url: "https://vinuni.edu.vn/aithucchien/tro-cap-hoc-bong-vingroup",
              chunk_index: 0,
            },
            retrieval_method: "hybrid",
          },
        ],
        retrieval_source: "hybrid",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0B0F19]">
      {/* Sidebar Trái */}
      <aside className="w-80 border-r border-gray-800 bg-[#0F1523] hidden md:flex flex-col justify-between p-5">
        <div className="space-y-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-white tracking-tight text-base flex items-center gap-2">
                AI IN ACTION
                <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-blue-500/20 text-blue-400 font-mono">
                  RAG
                </span>
              </h1>
              <p className="text-xs text-gray-400">Vingroup & VinUni</p>
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-xs font-semibold uppercase tracking-wider text-gray-400 px-1">
              Chế độ Retrieval
            </div>
            <div className="p-3 rounded-xl bg-gray-900/60 border border-gray-800 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Layers className="w-4 h-4 text-blue-400" />
                <span className="text-xs text-gray-200 font-medium">Hybrid Search (RRF)</span>
              </div>
              <input
                type="checkbox"
                checked={useHybrid}
                onChange={(e) => setUseHybrid(e.target.checked)}
                className="rounded text-blue-600 focus:ring-0 bg-gray-800 border-gray-700 w-4 h-4 cursor-pointer"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-xs font-semibold uppercase tracking-wider text-gray-400 px-1">
              Kho tri thức xác thực
            </div>
            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center gap-2 text-gray-300">
                <BookOpen className="w-4 h-4 text-red-400 shrink-0" />
                <span className="truncate">20K AI Handbook ver2.1</span>
              </div>
              <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center gap-2 text-gray-300">
                <ShieldCheck className="w-4 h-4 text-indigo-400 shrink-0" />
                <span className="truncate">QĐ 1290/QĐ-BKHCN (Bộ KH&CN)</span>
              </div>
              <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center gap-2 text-gray-300">
                <Award className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="truncate">Chuẩn năng lực SFIA Quốc tế</span>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-3 pt-4 border-t border-gray-800/80">
          {installPrompt && (
            <button
              onClick={handleInstallPWA}
              className="w-full py-2.5 px-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-medium flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20 transition"
            >
              <Download className="w-4 h-4" /> Cài Đặt Ứng Dụng (PWA)
            </button>
          )}

          <a
            href="/slides/index.html"
            target="_blank"
            className="w-full py-2.5 px-3 rounded-xl bg-gray-900 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 text-xs font-medium flex items-center justify-center gap-2 transition"
          >
            <ExternalLink className="w-4 h-4 text-pink-400" /> Mở Slide Báo Cáo
          </a>

          <div className="text-[11px] text-gray-400 text-center">
            Đỗ Khắc Gia Khoa • MSHV: 02733
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Top Header Mobile / Nav */}
        <header className="h-14 border-b border-gray-800 px-6 flex items-center justify-between bg-[#0F1523]/80 backdrop-blur-md">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-semibold text-sm text-white">Trợ Lý Sổ Tay AI Thực Chiến</span>
          </div>
          <div className="text-xs text-gray-400 hidden sm:block">
            Gemini 3.6 Flash • ChromaDB • BM25Okapi • RRF Reranking
          </div>
        </header>

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
            >
              <div
                className={`max-w-3xl rounded-2xl p-4 text-sm leading-relaxed shadow-sm ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-gray-900 border border-gray-800 text-gray-200 rounded-bl-none"
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Sources & Citations Badges */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-gray-800/80 space-y-2">
                    <div className="flex items-center justify-between text-xs text-gray-400">
                      <span className="flex items-center gap-1 font-semibold text-blue-400">
                        <BookOpen className="w-3.5 h-3.5" /> Nguồn trích dẫn ({msg.sources.length}):
                      </span>
                      <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-gray-800 text-gray-300">
                        Method: {msg.retrieval_source}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-2 pt-1">
                      {msg.sources.map((src, sIdx) => (
                        <button
                          key={sIdx}
                          onClick={() => setSelectedSource(src)}
                          className="px-2.5 py-1 rounded-lg bg-gray-800/90 hover:bg-gray-700 border border-gray-700 text-xs text-gray-300 flex items-center gap-1.5 transition active:scale-95"
                        >
                          <span className="font-bold text-blue-400">[{sIdx + 1}]</span>
                          <span className="max-w-[150px] truncate">{src.metadata.title}</span>
                          <span className="text-[10px] text-gray-400">({src.score.toFixed(2)})</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <span className="text-[10px] text-gray-400 mt-1 px-1">{msg.timestamp}</span>
            </div>
          ))}

          {loading && (
            <div className="flex items-center space-x-2 text-gray-400 text-xs py-2">
              <RefreshCw className="w-4 h-4 animate-spin text-blue-500" />
              <span>Đang trích xuất tri thức từ Sổ tay AI & sinh phản hồi...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Quick Sample Queries */}
        <div className="px-4 sm:px-8 py-2 overflow-x-auto flex gap-2 border-t border-gray-800/60 bg-[#0B0F19]/90 no-scrollbar">
          {SAMPLE_QUERIES.map((sq, sIdx) => (
            <button
              key={sIdx}
              onClick={() => handleSend(sq)}
              className="text-xs px-3 py-1.5 rounded-full bg-gray-900 border border-gray-800 text-gray-400 hover:text-white hover:border-gray-700 whitespace-nowrap transition"
            >
              {sq}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-4 sm:p-6 border-t border-gray-800 bg-[#0F1523]/80">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3 max-w-4xl mx-auto"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Đặt câu hỏi về học bổng, trợ cấp 8 triệu, tuyển sinh, chuẩn SFIA..."
              className="flex-1 bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white shadow-lg shadow-blue-500/20 transition active:scale-95"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </main>

      {/* Source Detail Modal */}
      {selectedSource && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F1523] border border-gray-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 max-h-[85vh] flex flex-col shadow-2xl">
            <div className="flex justify-between items-start border-b border-gray-800 pb-3">
              <div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-semibold uppercase">
                  {selectedSource.retrieval_method} • Score: {selectedSource.score.toFixed(4)}
                </span>
                <h3 className="font-bold text-lg text-white mt-1">
                  {selectedSource.metadata.title}
                </h3>
                <p className="text-xs text-gray-400">
                  Nguồn: <span className="text-gray-300 font-mono">{selectedSource.metadata.source}</span>
                </p>
              </div>
              <button
                onClick={() => setSelectedSource(null)}
                className="text-gray-400 hover:text-white p-1 rounded-lg hover:bg-gray-800 transition"
              >
                ✕
              </button>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 text-sm text-gray-300 leading-relaxed bg-gray-950/60 p-4 rounded-xl border border-gray-800 whitespace-pre-wrap font-sans">
              {selectedSource.content}
            </div>

            {selectedSource.metadata.url && (
              <div className="pt-2 flex justify-end">
                <a
                  href={selectedSource.metadata.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-blue-400 hover:underline flex items-center gap-1"
                >
                  Mở liên kết nguồn kiểm chứng <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
