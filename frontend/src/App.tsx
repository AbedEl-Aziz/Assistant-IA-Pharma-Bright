import { useState } from "react";
import ChatInput from "./components/ChatInput";
import ChatWindow from "./components/ChatWindow";
import SourcesPanel from "./components/SourcesPanel";
import Loader from "./components/Loader";
import { sendQuery } from "./services/api";

interface Message {
  question: string;
  answer: string;
  sources: string[];
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [tenantId, setTenantId] = useState<"tenant_a" | "tenant_b">("tenant_a");

  const handleSend = async (question: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await sendQuery(question, tenantId);

      setMessages((prev) => [
        ...prev,
        {
          question,
          answer: data.answer,
          sources: data.sources
        }
      ]);
    } catch (err) {
      setError("API request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 3, padding: "20px" }}>
        <h2>Assistant IA Pharma</h2>

        <select
          value={tenantId}
          onChange={(e) => setTenantId(e.target.value as "tenant_a" | "tenant_b")}
        >
          <option value="tenant_a">Tenant A</option>
          <option value="tenant_b">Tenant B</option>
        </select>

        {error && <p style={{ color: "red" }}>{error}</p>}
        {loading && <Loader />}

        <ChatWindow messages={messages} />
        <ChatInput onSend={handleSend} />
      </div>

      <SourcesPanel messages={messages} />
    </div>
  );
}

export default App;