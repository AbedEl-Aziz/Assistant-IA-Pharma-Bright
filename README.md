Pharma Regulatory RAG Assistant

Mini full-stack project implementing a RAG-based conversational assistant for pharmaceutical regulatory documents.
The system allows different tenants to query their own regulatory documents using natural language.

It includes:
- FastAPI backend
- LangChain RAG pipeline
- React frontend chat interface
- Multi-tenant document isolation
- API key authentication
- Query logging + metrics
- Unit tests
- Docker support

Project Structure
    pharma-rag-assistant/
    │
    ├── backend/
    │   ├── app/
    │   │   ├── core/
    │   │   ├── db/
    │   │   ├── documents/
    │   │   ├── models/
    │   │   ├── routers/
    │   │   ├── services/
    │   │   ├── utils/
    │   │   └── main.py
    │   │
    │   ├── tests/
    │   ├── .env
    │   └── requirements.txt
    │
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   ├── package.json
    │   └── vite.config.js
    │
    ├── Dockerfile
    ├── docker-compose.yml
    ├── README.md
    └── ARCHITECTURE.md

Prerequisites
    Install the following:
        Python 3.10+
        Node.js 18+
        Docker (optional)
        Git
        Download mistral-7b-instruct-v0.1.Q4_0.gguf from: (https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_0.gguf) 
            The file `mistral-7b-instruct-v0.1.Q4_0.gguf` is too large for GitHub.  
            Place it in the project directory before running scripts (path should be: backend\app\models\mistral-7b-instruct-v0.1.Q4_0.gguf).

Environment Variables
    cd backend
    Create a .env file from the example:
    cp .env .env

    Example .env:
    API_KEY_TENANT_A=key-tenant-a
    API_KEY_TENANT_B=key-tenant-b
    DATABASE_URL=postgresql://username:pass?@localhost:5432/dbName

ps: If you will use Docker move to the buttom of this file
else create a venv and install required libreries montionned in requirements.txt

Backend Setup (FastAPI) 
    Navigate to the backend directory using:
        cd backend
    Create virtual environment:
        python -m venv venv
    Activate it:
    if on Windows then
        venv\Scripts\activate
    Mac/Linux
        source venv/bin/activate
    Install dependencies:
        pip install -r requirements.txt
    Run the server:
        uvicorn app.main:app --reload
    Backend will run on:
    http://localhost:8000
     Swagger documentation:
    http://localhost:8000/docs

Frontend Setup (React)
    Navigate to the frontend folder:
        cd frontend
    Install dependencies:
        npm install
    Run the development server:
        npm run dev
    Frontend will run on:
        http://localhost:5173

API Usage
    Query Endpoint
        POST /query
    Example request:
        {
        "question": "What is the objective of ICH Q10?"
        }
    Header:
        X-API-Key: key-tenant-a
    Example response:
        {
        "answer": "...generated answer...",
        "sources": [
            {
            "document": "ich_q10.txt",
            "excerpt": "..."
            }
        ],
        "tenant_id": "tenant_a"
        }

Ingest Documents
    POST /documents/ingest
    Example request:
        tenant_id=tenant_a
        file=regulation.pdf
    Documents are indexed in the vector store for retrieval (backend/app/documents/tenant_a).

Metrics Endpoint
    GET /metrics/{tenant_id}
    Example request:
        tenant_id=tenant_a
    Example response:
        {
            "tenant_id": "tenant_a",
            "total_queries": 12,
            "average_duration_ms": 31794
        }

Running Tests
    Run unit tests with pytest:
        cd backend
        pytest or python -m pytest tests
    Example tests included:
        RAG pipeline response test
        Multi-tenant isolation test

Running with Docker
    Build the container:
        docker build -t pharma-rag .
    Run the container:
        docker run -p 8000:8000 pharma-rag

Example Workflow
    1-Start backend
    2-Start frontend
    3-Ask questions via the chat UI
    4-Upload documents with /documents/ingest
    5️-Inspect metrics via /metrics/{tenant_id}

Technologies Used
    Backend: FastAPI
    RAG: LangChain
    LLM: Mistral / GPT4All
    Vector Store: Chromas
    Frontend: React + Vite
    Database: PostgreSQL
    Testing: Pytest
    Containerization: Docker

Author
    Technical test project for Full-Stack Developer position – B'right Tunisia.
    made by AbedEl-Aziz Abouda

Date
    05/03/2026
