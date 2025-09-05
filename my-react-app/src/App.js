import React, { useState } from "react";
import { generateResponse } from "./api";

const App = () => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) {
      setResponse("Please enter a query.");
      return;
    }
    try {
      const result = await generateResponse({ input });
      setResponse(result.response); // Access the 'response' key from the result
    } catch (error) {
      console.error("Error:", error);
      setResponse("An error occurred while generating the response.");
    }
  };

  return (
    <div>
      <h1>React and Flask Integration</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Generate</button>
      </form>
      {response && <div>Response: {response}</div>}
    </div>
  );
};

export default App;
