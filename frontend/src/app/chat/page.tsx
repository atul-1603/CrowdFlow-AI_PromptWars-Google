"use client";

import ChatBox from "@/components/ChatBox";

export default function ChatPage() {
  return (
    <div className="h-full p-8 flex flex-col max-w-4xl mx-auto animate-in fade-in duration-500">
      <header className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight text-foreground">AI Assistant</h1>
        <p className="text-muted-foreground mt-1">Chat with Vertex AI to get smart recommendations</p>
      </header>

      <div className="flex-1 min-h-[500px]">
        <ChatBox />
      </div>
    </div>
  );
}
