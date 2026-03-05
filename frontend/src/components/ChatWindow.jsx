function ChatWindow({ messages }) {
  return (
    <div style={{ marginTop: "20px" }}>
      {messages.map((msg, index) => (
        <div key={index} style={{ marginBottom: "15px" }}>
          <strong>Question:</strong>
          <p>{msg.question}</p>

          <strong>Answer:</strong>
          <p>{msg.answer}</p>
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;