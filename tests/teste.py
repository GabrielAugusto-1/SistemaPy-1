import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        yield client


def test_listar_clientes(client):
    response = client.get("/clientes")
    
    assert response.status_code == 200


def test_criar_cliente(client):
    response = client.post("/clientes", json={
        "nome": "Teste",
        "email": "teste@email.com",
        "senha": "123"
    })

    data = response.get_json()

    assert data["Mensagem"] == "Usuario validado e cadastrado com sucesso!"