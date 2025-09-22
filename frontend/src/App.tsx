import { useState } from "react";
import { Header } from "./components/Header";
import { ConversationArea } from "./components/ConversationArea";
import { VoiceInputBar } from "./components/VoiceInputBar";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = async (text: string) => {
    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Send to backend API for AI answer
    try {
      const resp = await fetch("http://localhost:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!resp.ok) {
        throw new Error(`Server error: ${resp.status}`);
      }
      const data = await resp.json();
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer ?? "No answer received.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (err: any) {
      const errMsg: Message = {
        id: (Date.now() + 2).toString(),
        text: "Error contacting backend: " + (err?.message || String(err)),
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errMsg]);
    }
  };

  return (
    <div className="h-screen w-full max-w-[1440px] mx-auto flex flex-col bg-background">
      <Header />
      <ConversationArea messages={messages} />
      <VoiceInputBar onSendMessage={handleSendMessage} />
    </div>
  );
}
