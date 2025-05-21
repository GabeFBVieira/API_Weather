import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app, items_db  

client = TestClient(app)

def setup_function():
    items_db.clear() 

def test_get_temperaturas_inicial_vazio():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

def test_adicionar_cidade_com_clima():
    cidade = {
        "id": 1,
        "name": "São Paulo",
        "description": "Chuva e garoa 18°C"
    }
    response = client.post("/items", json=cidade)
    assert response.status_code == 200
    assert response.json() == cidade

def test_get_cidades_depois_do_post():
   
    cidade = {
        "id": 2,
        "name": "Florianopolis",
        "description": "Frio de 03°C ❄️"
    }
    client.post("/items", json=cidade)

   
    response = client.get("/items")
    assert response.status_code == 200
    cidades = response.json()
    assert isinstance(cidades, list)
    assert len(cidades) == 1
    assert cidades[0]["name"] == "Florianopolis"
    assert "03°C" in cidades[0]["description"]
