def test_create_movement_in(client, operator_token, product_id):
    response = client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={
            "type": "IN",
            "quantity": 10,
            "product_id": product_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 10
    assert data["type"] == "IN"

def test_create_movement_out(client, operator_token, product_id):
    # Primero IN para tener stock
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "IN", "quantity": 20, "product_id": product_id}
    )

    # Ahora OUT
    response = client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 5, "product_id": product_id}
    )

    assert response.status_code == 200
    assert response.json()["type"] == "OUT"


def test_movement_out_insufficient_stock(client, operator_token, product_id):
    response = client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 999, "product_id": product_id}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock"



def test_stock_updates_correctly(client, operator_token, admin_token, product_id):
    # IN 30
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "IN", "quantity": 30, "product_id": product_id}
    )

    # OUT 10
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 10, "product_id": product_id}
    )

    # Consultar producto
    product = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    ).json()

    assert product["quantity"] == 20


def test_product_history(client, operator_token, product_id):
    # Crear movimientos
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "IN", "quantity": 5, "product_id": product_id}
    )
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 2, "product_id": product_id}
    )

    # Obtener historial
    response = client.get(
        f"/api/v1/products/{product_id}/history",
        headers={"Authorization": f"Bearer {operator_token}"}
    )

    assert response.status_code == 200
    history = response.json()
    assert len(history) >= 2
    assert history[0]["type"] == "IN"
    assert history[1]["type"] == "OUT"


def test_list_all_movements_requires_supervisor_or_admin(client, operator_token):
    response = client.get(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    assert response.status_code == 403

def test_stock_increases_with_in_movement(client, operator_token, admin_token, product_id):
    # Movimiento IN
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "IN", "quantity": 15, "product_id": product_id}
    )

    # Consultar producto
    response = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product = response.json()

    assert product["quantity"] == 15


def test_stock_decreases_with_out_movement(client, operator_token, admin_token, product_id):
    # IN para tener stock
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "IN", "quantity": 20, "product_id": product_id}
    )

    # OUT
    client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 5, "product_id": product_id}
    )

    # Consultar producto
    response = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product = response.json()

    assert product["quantity"] == 15

def test_stock_cannot_go_negative(client, operator_token, product_id):
    response = client.post(
        "/api/v1/movements/",
        headers={"Authorization": f"Bearer {operator_token}"},
        json={"type": "OUT", "quantity": 999, "product_id": product_id}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock"

    