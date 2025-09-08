import React, { useState, useRef, useEffect } from "react";
import { generateResponse } from "./api";
import "./App.css";
import ChatInput from "./components/ChatInput";
import ChatContainer from "./components/ChatContainer";
import LoadingIndicator from "./components/LoadingIndicator";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);
  const chatEndRef = useRef(null);

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

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const cleanedInput = input.replace(/\s+/g, " ").trim();

    setMessages((prev) => [...prev, { role: "user", content: cleanedInput }]);
    setInput("");
    setLoading(true);

    try {
      const result = await generateResponse({ input: cleanedInput });
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
    <div className="app-container">
      <h1>Q&AI Helper</h1>
      <ChatInput
        input={input}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
        textareaRef={textareaRef}
        loading={loading}
      />
      {loading && <LoadingIndicator />}
      {messages.length > 0 && (
        <ChatContainer messages={messages} chatEndRef={chatEndRef} />
      )}
    </div>
  );
};

export default App;
