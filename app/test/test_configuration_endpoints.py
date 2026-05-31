import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Añadir el directorio raíz de este microservicio al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi.testclient import TestClient
from app.main import app
from app.routers.business_profile_router import get_db

# Mock de la sesión de base de datos de SQLAlchemy
mock_db_session = MagicMock()

def override_get_db():
    yield mock_db_session

@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)
    mock_db_session.reset_mock()

def test_configuration_health():
    client = TestClient(app)
    response = client.get("/api/v1/configuration/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "ms-CONFIGURATION"

def test_create_profile_success():
    client = TestClient(app)
    
    payload = {
        "nombre_perfil": "Perfil Inmobiliario",
        "peso_poblacion": 0.4,
        "peso_ingresos": 0.3,
        "peso_competencia": 0.3,
        "is_active": True
    }
    
    # Configurar el objeto que retorna db.refresh para tener todos los campos del response_model
    mock_profile_obj = MagicMock()
    mock_profile_obj.id = 1
    mock_profile_obj.nombre_perfil = payload["nombre_perfil"]
    mock_profile_obj.peso_poblacion = payload["peso_poblacion"]
    mock_profile_obj.peso_ingresos = payload["peso_ingresos"]
    mock_profile_obj.peso_competencia = payload["peso_competencia"]
    mock_profile_obj.is_active = payload["is_active"]
    
    # db.refresh(db_profile) actualiza el objeto en-sitio; simulamos eso configurando el side_effect
    def fake_refresh(obj):
        obj.id = 1
        obj.nombre_perfil = payload["nombre_perfil"]
        obj.peso_poblacion = payload["peso_poblacion"]
        obj.peso_ingresos = payload["peso_ingresos"]
        obj.peso_competencia = payload["peso_competencia"]
        obj.is_active = payload["is_active"]
    
    mock_db_session.refresh.side_effect = fake_refresh
    
    response = client.post("/api/v1/configuration/profiles/", json=payload)
    assert response.status_code == 200
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_create_profile_value_error_validation():
    client = TestClient(app)
    
    # Pesos que no suman 1.0 -> Factory lanzará ValueError
    payload = {
        "nombre_perfil": "Perfil Inválido",
        "peso_poblacion": 0.9,
        "peso_ingresos": 0.5,
        "peso_competencia": 0.3,
        "is_active": True
    }
    
    response = client.post("/api/v1/configuration/profiles/", json=payload)
    assert response.status_code == 400
    # Mensaje exacto del BusinessProfileFactory
    assert "La suma de los pesos debe ser igual a 1.0" in response.json()["detail"]

def test_get_profiles():
    client = TestClient(app)
    
    mock_profile = MagicMock()
    mock_profile.id = 1
    mock_profile.nombre_perfil = "Perfil Test"
    mock_profile.peso_poblacion = 0.4
    mock_profile.peso_ingresos = 0.3
    mock_profile.peso_competencia = 0.3
    mock_profile.is_active = True
    
    mock_db_session.query().all.return_value = [mock_profile]
    
    response = client.get("/api/v1/configuration/profiles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre_perfil"] == "Perfil Test"

def test_get_active_profile_not_found():
    client = TestClient(app)
    
    mock_db_session.query().filter().first.return_value = None
    
    response = client.get("/api/v1/configuration/profiles/active")
    assert response.status_code == 404
    assert response.json()["detail"] == "No hay perfil activo"
