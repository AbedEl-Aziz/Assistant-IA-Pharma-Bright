function SourcesPanel({ messages }) {
  if (messages.length === 0) return null;

  const lastMessage = messages[messages.length - 1];

  return (
    <div style={{
      flex: 1,
      borderLeft: "1px solid #ccc",
      padding: "20px",
      overflowY: "auto"
    }}>
      <h3>Sources</h3>

      {lastMessage.sources.map((source, index) => (
        <div key={index} style={{ marginBottom: "15px" }}>
          <strong>{source.source}</strong>
          <p>{source.text}</p>
        </div>
      ))}
    </div>
  );
}

export default SourcesPanel;