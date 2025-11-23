import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_items_empty():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    item_data = {"name": "Test Item", "description": "Test Description"}
    response = client.post("/api/items", json=item_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
    assert "id" in response.json()

def test_get_item_by_id():
    # Crear item
    item_data = {"name": "Test Item 2", "description": "Desc 2"}
    create_response = client.post("/api/items", json=item_data)
    item_id = create_response.json()["id"]
    
    # Obtener item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == "Test Item 2"

def test_get_nonexistent_item():
    response = client.get("/api/items/99999")
    assert response.status_code == 404