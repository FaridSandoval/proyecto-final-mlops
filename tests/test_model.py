from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    """
    Prueba básica: Verificar que la API arranca y sirve el HTML correctamente.
    """
    response = client.get("/")
    
    # 1. Verificar que la respuesta es exitosa (Código 200)
    assert response.status_code == 200
    
    # 2. Verificar que recibimos contenido (la página web)
    # Ya no usamos .json() porque ahora es HTML
    assert response.content