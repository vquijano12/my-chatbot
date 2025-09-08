import React, { useState, useRef, useEffect } from "react";
import { generateResponse } from "./api";
import "./App.css";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto"; // Reset height
      textarea.style.height = textarea.scrollHeight + "px"; // Auto-expand
      textarea.focus(); // Refocus
    }
  }, [input]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");
    setLoading(true);

    try {
      const result = await generateResponse({ input });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result.response },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "An error occurred while generating the response.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Q&AI Helper</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInputChange}
          rows={1}
          className="chat-input"
          style={{ resize: "none" }}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
      {loading && (
        <div className="loading-indicator">
          <span className="spinner"></span> Generating response...
        </div>
      )}
      <div className="chat">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.role === "user" ? "user-row" : "assistant-row"}
          >
            <div
              className={
                msg.role === "user" ? "user-message" : "assistant-message"
              }
            >
              <b>{msg.role === "user" ? "You" : "Bot"}:</b> {msg.content}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
