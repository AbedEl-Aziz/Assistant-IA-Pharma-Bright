from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

API_KEYS = {
    os.getenv("API_KEY_TENANT_A"): "tenant_a",
    os.getenv("API_KEY_TENANT_B"): "tenant_b",
}

def verify_api_key(x_api_key: str = Header(...)):
    tenant_id = API_KEYS.get(x_api_key)
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return tenant_id