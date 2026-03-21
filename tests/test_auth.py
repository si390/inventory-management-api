def test_register_user(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "123456",
            "role": "operator"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"


def test_login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "123456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_refresh_token(client):
    # Login primero
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "123456"}
    )
    refresh_token = login.json()["refresh_token"]

    # Usar refresh token
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_token_invalid(client):
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalidtoken123"}
    )
    assert response.status_code == 401