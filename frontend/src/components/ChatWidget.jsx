import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, User, Sparkles, AlertCircle } from 'lucide-react';
import { apiClient } from '../api/client';

export default function ChatWidget({ parcelId }) {
  if (!parcelId) return null;

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: "Hello! I am your TerraLux AI agronomic assistant. I can analyze soil physics, justify resilient crop selection via NASA POWER and SoilGrids, or assess economic yield and disease risks for this parcel.",
      tool_calls: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (textToSend) => {
    const q = textToSend || input;
    if (!q.trim() || loading) return;

    const userMsg = { role: 'user', text: q };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await apiClient.post('/chat', {
        message: q,
        parcel_id: parcelId
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: res.data.response,
          tool_calls: res.data.tool_calls || []
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: "Sorry, a network connection error occurred while querying the agronomic engine.",
          tool_calls: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Floating button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2 px-4 py-3 bg-forest hover:bg-forest-light text-sand rounded-full shadow-2xl transition-all transform hover:scale-105 border border-forest-light/40 group"
        >
          <Bot className="w-5 h-5 text-accent animate-pulse" />
          <span className="font-semibold text-sm">Agronomic AI Assistant</span>
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div className="w-[360px] sm:w-[420px] h-[550px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-200">
          
          {/* Header */}
          <div className="bg-forest text-white p-4 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-forest-light flex items-center justify-center text-accent">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-sand flex items-center gap-2">
                  TerraLux AI Assistant
                  <span className="text-[10px] bg-accent/90 px-1.5 py-0.5 rounded text-white font-mono">
                    Grounded
                  </span>
                </h3>
                <p className="text-[11px] text-white/70">Fusing NASA POWER & SoilGrids</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/70 hover:text-white p-1 rounded-lg hover:bg-white/10"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Quick Suggestions */}
          <div className="bg-sand/30 px-3 py-2 border-b border-sand-dark/20 flex gap-1.5 overflow-x-auto text-[11px] whitespace-nowrap">
            <button
              onClick={() => handleSend("Why recommend this crop?")}
              className="px-2.5 py-1 bg-white hover:bg-forest/5 text-forest rounded-full border border-forest/20 shadow-xs"
            >
              🌱 Why this crop?
            </button>
            <button
              onClick={() => handleSend("What is the soil pH?")}
              className="px-2.5 py-1 bg-white hover:bg-forest/5 text-forest rounded-full border border-forest/20 shadow-xs"
            >
              🧪 Soil pH & Fertility
            </button>
            <button
              onClick={() => handleSend("What is the expected yield and margin?")}
              className="px-2.5 py-1 bg-white hover:bg-forest/5 text-forest rounded-full border border-forest/20 shadow-xs"
            >
              🌾 Yield & Margin
            </button>
            <button
              onClick={() => handleSend("I noticed a spot on the leaves")}
              className="px-2.5 py-1 bg-white hover:bg-forest/5 text-forest rounded-full border border-forest/20 shadow-xs"
            >
              🍂 Leaf Diagnosis
            </button>
          </div>

          {/* Message history — Zero internal tool badges displayed */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-50/50">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed shadow-xs ${
                    m.role === 'user'
                      ? 'bg-forest text-white rounded-br-none'
                      : 'bg-white text-gray-800 border border-gray-200/80 rounded-bl-none'
                  }`}
                >
                  {m.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 text-xs text-forest/70 font-medium">
                <Sparkles className="w-4 h-4 animate-spin text-accent" />
                <span>Consulting verified scientific databases...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-white border-t border-gray-200 flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask your agronomic or financial question..."
              className="flex-1 bg-gray-100 border border-gray-300 rounded-xl px-3.5 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-forest focus:bg-white text-gray-900 placeholder:text-gray-500"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-accent hover:bg-accent-dark disabled:opacity-50 text-white p-2.5 rounded-xl shadow-md transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

        </div>
      )}
    </div>
  );
}
