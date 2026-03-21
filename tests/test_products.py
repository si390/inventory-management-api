def test_operator_cannot_create_product(client, operator_token):
    response = client.post(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={
            "name": "Mouse",
            "quantity": 10,
            "price": 20.0
        }
    )
    assert response.status_code == 403


def test_admin_can_create_product(client, admin_token):
    response = client.post(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Keyboard",
            "quantity": 5,
            "price": 50.0
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Keyboard"
    assert data["quantity"] == 5


def test_get_product_by_id(client, admin_token, product_id):
    response = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id

def test_list_products(client, admin_token):
    response = client.get(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)