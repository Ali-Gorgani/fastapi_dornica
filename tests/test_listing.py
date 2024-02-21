def test_create_listing(client_with_auth):
    response = client_with_auth.post("/listings/", json={
        "type": "HOUSE",
        "address": "123 Test St",
        # Add other fields as necessary
    })
    assert response.status_code == 201
