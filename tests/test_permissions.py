def test_operator_cannot_create_users(client):
    # Login como operador
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "123456"}
    )
    token = login.json()["access_token"]

    # Intentar crear usuario
    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "new@example.com",
            "password": "123456",
            "role": "operator"
        }
    )
    assert response.status_code == 403


def test_admin_can_create_users(client):
    # Crear admin
    client.post(
        "/api/v1/users/",
        json={
            "email": "admin@example.com",
            "password": "admin123",
            "role": "admin"
        }
    )

    # Login admin
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    token = login.json()["access_token"]

    # Crear usuario nuevo
    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "user2@example.com",
            "password": "123456",
            "role": "operator"
        }
    )
    assert response.status_code == 201