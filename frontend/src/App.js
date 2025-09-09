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
  const [showScrollBtn, setShowScrollBtn] = useState(false);
  const chatContainerRef = useRef(null);

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

  useEffect(() => {
    const chatContainer = chatContainerRef.current;
    if (!chatContainer) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = chatContainer;
      setShowScrollBtn(scrollTop + clientHeight < scrollHeight - 20);
    };

    chatContainer.addEventListener("scroll", handleScroll);

    // Run once in case the chat is already scrollable
    handleScroll();

    // Clean up
    return () => chatContainer.removeEventListener("scroll", handleScroll);
  }, [messages]); // <-- add messages as a dependency

  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

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
      let errorMessage =
        "An unexpected error has occurred while generating the response.";
      if (error.response) {
        // Server responded with a status code outside 2xx
        errorMessage = `Server error (${error.response.status}): ${
          error.response.data?.error || "Please try again later."
        }`;
      } else if (error.request) {
        // Request was made but no response received (server down or unreachable)
        errorMessage =
          "Unable to connect to the server. Please make sure the server is running.";
      } else if (error.message) {
        // Something else happened
        errorMessage = `Error: ${error.message}`;
      }
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: errorMessage,
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
        <div style={{ position: "relative" }}>
          <ChatContainer
            messages={messages}
            chatEndRef={chatEndRef}
            chatContainerRef={chatContainerRef}
            scrollToBottom={scrollToBottom}
            showScrollBtn={showScrollBtn}
          />
        </div>
      )}
    </div>
  );
};

export default App;
