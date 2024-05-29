from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    response = client.post("/api/v1/order/", json={
        "document_no": "123",
        "customer": "John Doe",
        "details": [{
            "product": "Product 1",
            "qty": 10,
            "price": 100.0,
            "subtotal": 1000.0,
            "discount_per_item": 10.0,
            "after_discount": 900.0,
            "tax": 90.0,
            "after_tax": 990.0
        }]
    })
    assert response.status_code == 200
    assert response.json()["document_no"] == "123"
