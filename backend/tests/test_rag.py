def test_rag_pipeline_returns_answer(client):

    from io import BytesIO

    file_content = b"ICH Q10 defines a Pharmaceutical Quality System."
    file_like = BytesIO(file_content)

    ingest_response = client.post(
        "/documents/ingest",
        data={"tenant_id": "tenant_b"},
        files={"file": ("test_doc.txt", file_like, "text/plain")},
        headers={"X-API-Key": "key-tenant-b"}
    )

    assert ingest_response.status_code == 200

    response = client.post(
        "/query",
        json={"question": "What does ICH Q10 define?"},
        headers={"X-API-Key": "key-tenant-a"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] is not None
    assert len(data["answer"]) > 0
    assert len(data["sources"]) > 0