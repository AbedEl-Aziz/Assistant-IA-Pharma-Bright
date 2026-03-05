import axios from "axios";

const API_URL = "http://127.0.0.1:8000/query";

export const sendQuery = async (question, tenantId) => {
  const apiKey = tenantId === "tenant_a" ? "key-tenant-a" : "key-tenant-b";

  const response = await axios.post(
    API_URL,
    { question },
    {
      headers: {
        "X-API-Key": apiKey,
        "Content-Type": "application/json"
      }
    }
  );

  return response.data;
};