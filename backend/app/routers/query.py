from fastapi import APIRouter, Depends
from app.models.request_models import QuestionRequest
from app.services.rag_pipeline import RagPipeline
from app.core.security import verify_api_key

router = APIRouter(prefix="/query", tags=["Query"])
rag_pipeline = RagPipeline()

@router.post("/")
async def query_question(
    request: QuestionRequest,
    tenant_id: str = Depends(verify_api_key)
):
    response = rag_pipeline.run(
        question=request.question,
        tenant_id=tenant_id
    )

    return {
        "tenant_id": tenant_id,
        "answer": response["answer"] if response["answer"] else [],
        "sources": response["sources"]
    }