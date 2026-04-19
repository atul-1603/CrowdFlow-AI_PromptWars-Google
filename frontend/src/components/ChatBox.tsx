"use client";

import { useChat } from "@/lib/hooks";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, AlertCircle } from "lucide-react";

export default function ChatBox() {
  const { chatHistory, sendMessage, isTyping, error } = useChat();
  const [query, setQuery] = useState("");
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isTyping]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isTyping) return;
    sendMessage(query);
    setQuery("");
  };

  return (
    <div className="bg-card rounded-xl border border-border shadow-sm flex flex-col h-full overflow-hidden">
      <div className="p-4 border-b border-border bg-secondary/30 flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-accent to-primary flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.3)]">
          <Bot size={18} className="text-white" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-card-foreground">Vertex AI Assistant</h2>
          <p className="text-[10px] text-muted-foreground flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-success inline-block"></span> Online
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatHistory.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-60">
            <Bot size={40} className="mb-3 text-muted-foreground" />
            <p className="text-sm font-medium">Hello! I'm your stadium assistant.</p>
            <p className="text-xs mt-1 text-muted-foreground">Ask me for directions, queue times, or general advice.</p>
          </div>
        ) : (
          chatHistory.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm ${
                msg.role === 'user' 
                  ? 'bg-primary text-primary-foreground rounded-tr-sm shadow-[0_4px_10px_rgba(59,130,246,0.2)]' 
                  : 'bg-secondary text-secondary-foreground rounded-tl-sm border border-border/50'
              }`}>
                <p className="leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))
        )}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-secondary text-secondary-foreground rounded-2xl rounded-tl-sm px-4 py-3 border border-border/50 flex items-center gap-2">
              <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-center">
            <div className="bg-destructive/10 text-destructive border border-destructive/20 rounded-lg px-3 py-2 text-xs flex items-center gap-2">
              <AlertCircle size={14} />
              {error}
            </div>
          </div>
        )}
        
        <div ref={endOfMessagesRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-3 border-t border-border bg-background">
        <div className="relative flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask something..."
            className="w-full bg-input border border-border rounded-full pl-4 pr-12 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            disabled={isTyping}
          />
          <button 
            type="submit" 
            disabled={!query.trim() || isTyping}
            className="absolute right-1 w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-colors"
          >
            {isTyping ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
          </button>
        </div>
      </form>
    </div>
  );
}
