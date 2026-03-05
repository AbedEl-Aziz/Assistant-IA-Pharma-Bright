import { useState } from "react";

function ChatInput({ onSend }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    onSend(question);
    setQuestion("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a regulatory question..."
        style={{ width: "80%" }}
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default ChatInput;