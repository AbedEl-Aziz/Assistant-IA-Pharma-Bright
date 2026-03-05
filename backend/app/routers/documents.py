from fastapi import APIRouter, UploadFile, File, Form, Depends
from pathlib import Path
from app.core.security import verify_api_key

router = APIRouter(prefix="/documents", tags=["Documents"])

BASE_DOC_PATH = Path(__file__).parent.parent / "documents"

@router.post("/ingest")
async def ingest_document(
    tenant_id: str = Form(...),
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    tenant_folder = BASE_DOC_PATH / api_key
    tenant_folder.mkdir(parents=True, exist_ok=True)

    file_path = tenant_folder / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "Document uploaded", "tenant_id": tenant_id}