from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import query, documents, metrics
from app.db.database import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pharma AI Assistant")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(query.router)
app.include_router(documents.router)
app.include_router(metrics.router)