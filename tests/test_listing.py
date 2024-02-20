from app import schemas


# must deactivate allowed_client_ips section in main.py

def test_get_all_posts(authorized_client):
    response = authorized_client.get("/listings")


def test_get_one_post(authorized_client, test_listings):
    response = authorized_client.get(f"/listings/{test_listings[0].id}")
    listing = schemas.ListingOut(**response.json())
    assert response.status_code == 200
    assert listing.type == test_listings[0].type
    assert listing.address == test_listings[0].address
