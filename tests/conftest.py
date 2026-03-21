import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings


# Base de datos temporal para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Override de la dependencia get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_token(client):
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
    return login.json()["access_token"]


@pytest.fixture
def operator_token(client):
    # Crear operador
    client.post(
        "/api/v1/users/",
        json={
            "email": "op@example.com",
            "password": "op123",
            "role": "operator"
        }
    )
    # Login operador
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "op@example.com", "password": "op123"}
    )
    return login.json()["access_token"]


@pytest.fixture
def product_id(client, admin_token):
    # Crear producto
    response = client.post(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Laptop",
            "quantity": 0,
            "price": 1500
        }
    )
    return response.json()["id"]
