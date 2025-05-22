import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const chatBoxRef = useRef(null);
  const context = useRef([]);

  useEffect(() => {
    chatBoxRef.current?.scrollTo({
      top: chatBoxRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: [{ text: input }] };
    setMessages([...messages, { role: "user", content: input }]);

    context.current.push(userMessage);

    if (context.current.length > 10) {
      context.current.shift();
    }

    setInput("");

    try {
      const response = await axios.post("http://localhost:5050/chat", {
        context: context.current,
      });

      const botMessage = {
        role: "assistant",
        content: [{ text: response.data.response }]
      };

      setMessages((prev) => [...prev, botMessage]);
      context.current.push(botMessage);

      if (context.current.length > 10) {
        context.current.shift();
      }

    } catch (error) {
      console.error("Error:", error);

      const errorMessage = {
        role: "error",
        content: [{ text: "Unable to connect to the server. Please try again." }]
      };

      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="chat-header">Chat with AI</div>
        <div className="chat-box" ref={chatBoxRef}>
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              {msg.role === "user" ? (
                <p>{msg.content}</p>
              ) : (
                <ReactMarkdown>{msg.content[0].text}</ReactMarkdown>
              )}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;