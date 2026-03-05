def test_tenant_isolation(client):

    # Tenant A
    client.post(
        "/documents/ingest",
        data={"tenant_id": "tenant_a"},
        files={"file": ("tenant_a_doc.txt", b"Document belonging to tenant A.", "text/plain")},
        headers={"X-API-Key": "key-tenant-a"}
    )

    # Tenant B
    client.post(
        "/documents/ingest",
        data={"tenant_id": "tenant_b"},
        files={"file": ("tenant_b_doc.txt", b"Secret document belonging to tenant B.", "text/plain")},
        headers={"X-API-Key": "key-tenant-b"}
    )

    # Tenant A querie
    response = client.post(
        "/query",
        json={"question": "What is the secret document?"},
        headers={"X-API-Key": "key-tenant-a"}
    )

    data = response.json()

    for source in data["sources"]:
        assert "tenant B" not in source["text"]