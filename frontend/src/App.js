import React, { useState } from "react";
import { generateResponse } from "./api";
import "./App.css";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");

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
    }
  };

  return (
    <div>
      <h1>Q&AI Helper</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      <div>
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
