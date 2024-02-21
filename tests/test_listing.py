def test_create_listing(client_with_auth):
    response = client_with_auth.post("/listings/", json={
        "type": "HOUSE",
        "address": "123 Test St",
    })
    assert response.status_code == 201


def test_get_listings(client_with_auth):
    response = client_with_auth.get("/listings/1")
    assert response.status_code == 200


def test_update_listing(client_with_auth):
    response = client_with_auth.put("/listings/1", json={
        "type": "APARTMENT",
        "address": "123 Test St",
    })
    assert response.status_code == 200


def test_delete_listing(client_with_auth):
    response = client_with_auth.delete("/listings/1")
    assert response.status_code == 204
