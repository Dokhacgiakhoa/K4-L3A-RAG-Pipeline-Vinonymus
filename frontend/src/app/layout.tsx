import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sổ Tay AI Thực Chiến — Vingroup & VinUni",
  description: "Hệ thống Chatbot RAG tra cứu cẩm nang tuyển sinh, học bổng 100%, chuẩn SFIA và lộ trình đào tạo nhân tài AI",
  manifest: "/manifest.json",
  themeColor: "#2563eb",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "AI Thực Chiến",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="/favicon.ico" sizes="any" />
      </head>
      <body className="antialiased min-h-screen bg-[#0B0F19] text-gray-100">
        {children}
      </body>
    </html>
  );
}
