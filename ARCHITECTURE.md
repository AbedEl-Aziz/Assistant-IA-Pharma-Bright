# Architecture Overview

# 1. System Overview

The system implements a Retrieval-Augmented Generation (RAG) assistant for querying pharmaceutical regulatory documents.
It follows a modular full-stack architecture composed of three main layers:

* Frontend (React) — User chat interface
* Backend API (FastAPI) — Request orchestration, authentication, and logging
* AI Retrieval Pipeline (LangChain) — Document indexing, retrieval, and answer generation

The design emphasizes:

* Clear separation of concerns
* Multi-tenant isolation
* Traceability of responses
* Extensibility for production environments

---

# 2. High-Level Architecture

```
User
  │
  ▼
React Frontend (Chat UI)
  │
  ▼
FastAPI Backend
  │
  ├── Authentication (API Key)
  ├── Query Logging (SQL)
  ├── Tenant Isolation
  │
  ▼
RAG Pipeline (LangChain)
  │
  ├── Document Chunking
  ├── Embeddings
  ├── Vector Store (Chroma)
  │
  ▼
Retriever
  │
  ▼
LLM (Mistral / GPT4All)
  │
  ▼
Generated Answer + Sources
```

---

# 3. Backend Architecture

The backend is structured using FastAPI routers and service layers.

## API Layer

Routes are grouped by domain:

| Endpoint               | Responsibility            |
| ---------------------- | ------------------------- |
| `/query`               | Executes the RAG pipeline |
| `/documents/ingest`    | Indexes new documents     |
| `/metrics/{tenant_id}` | Returns usage statistics  |

Each request is authenticated using an API Key in the `X-API-Key` header.

---

## Service Layer

Business logic is isolated in services:

## RAG Pipeline

Responsible for:

* loading documents
* chunking text
* generating embeddings
* retrieving relevant context
* generating responses

This layer ensures that the API layer remains thin and maintainable.

---

## Data Layer

The data layer manages persistence and logging.

## Database

PostgreSQL is used for simplicity.

The table `query_logs` stores:

| Field       | Description         |
| ----------- | ------------------- |
| timestamp   | request time        |
| tenant_id   | requesting tenant   |
| question    | user query          |
| nb_sources  | retrieved documents |
| duration_ms | pipeline latency    |

This enables basic observability and metrics.

---

# 4. RAG Pipeline Design

The RAG pipeline follows a typical sequence:

1. Document Ingestion

Documents are uploaded through `/documents/ingest` and processed as:

```
Document
  → Text extraction
  → Chunking
  → Embedding
  → Vector storage
```

Chunking strategy:

* chunk size: ~500 characters
* overlap: ~100 characters

This improves retrieval quality while preserving context.

---

2. Query Processing

When a query is received:

```
User Question
  → Embed question
  → Retrieve top-k similar chunks
  → Inject chunks into LLM prompt
  → Generate answer
```

The system returns:

* Generated answer
* Document sources
* Extracted context

This provides traceability of AI outputs, which is important in regulated environments.

---

# 5. Multi-Tenant Isolation

Tenant isolation is implemented at the vector store and query level.

Each document is stored with metadata:

```
tenant_id
document_name
chunk_id
```

During retrieval, the pipeline filters vectors using:

```
metadata.tenant_id == request.tenant_id
```

This ensures that tenants cannot access documents belonging to other tenants.

---

# 6. Security

Security mechanisms implemented:

### API Key Authentication

Each tenant is assigned an API key.

Requests must include:

```
X-API-Key: <tenant_key>
```

The backend validates the key and resolves the associated `tenant_id`.

---

# 7. Frontend Design

The React frontend provides a minimal chat interface.

Features:

* Question input
* Response display
* Source document visualization
* Loading and error states

The frontend communicates with the backend via REST API.

---

# 8. Observability

Basic monitoring is implemented using query logging.

Metrics endpoint:

* GET /metrics/{tenant_id}

Returns:

* number of queries
* average response time

This allows simple monitoring of system usage.

# 9. Possible Improvements

Several improvements would be required for production deployment.
Scalability

* Replace SQLite with PostgreSQL
* Use a distributed vector database (Weaviate / Pinecone)

Performance

* Add embedding caching
* Use async pipelines

Security

* Replace API keys with OAuth / JWT
* Implement rate limiting

RAG Quality

* Hybrid retrieval (keyword + vector)
* Reranking models
* Prompt optimization

# Conclusion

The architecture prioritizes clarity, modularity, and traceability, which are essential for AI systems operating in regulated pharmaceutical environments.
The modular design allows easy evolution toward production-grade infrastructure.