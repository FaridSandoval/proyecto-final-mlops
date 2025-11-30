from fastapi.testclient import TestClient
from src.app import app

# Creamos un cliente de prueba (como un navegador falso)
client = TestClient(app)

def test_read_root():
    """
    Prueba básica: Verificar que la API arranca y responde en la ruta principal.
    Esto cumple con la etapa 'Test' del pipeline.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Iris MLOps Activa"}


# Suite de pruebas unitarias para validación de inferencia