import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from app.main import app
from app.core.llm_factory import get_llm
from app.core.config import settings

client = TestClient(app)


def test_read_root():
    """Prueba el endpoint raíz de la API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Autonomous Multi-Tool Agent API"


@patch("app.main.agent_app.ainvoke")
def test_chat_endpoint_text_only(mock_ainvoke):
    """Prueba el endpoint de chat enviando solo texto."""
    # Simulamos la respuesta del agente
    mock_ainvoke.return_value = {
        "messages": [AIMessage(content="Hola, soy tu agente.", name="agent")]
    }

    response = client.post("/chat", data={"query": "Hola"})
    assert response.status_code == 200
    assert response.json()["response"] == "Hola, soy tu agente."


@patch("app.main.agent_app.ainvoke")
def test_chat_endpoint_with_image(mock_ainvoke):
    """Prueba el endpoint de chat enviando texto e imagen."""
    mock_ainvoke.return_value = {
        "messages": [AIMessage(content="Veo una imagen.", name="agent")]
    }

    # Simulamos un archivo
    file_content = b"fake image bytes"
    files = {"image": ("test.jpg", file_content, "image/jpeg")}
    data = {"query": "Analiza esto"}

    response = client.post("/chat", data=data, files=files)
    assert response.status_code == 200
    assert response.json()["response"] == "Veo una imagen."


def test_llm_factory_openrouter():
    """Prueba el Patrón Factory para OpenRouter."""
    with patch.object(settings, "LLM_PROVIDER", "OPENROUTER"):
        llm = get_llm()
        assert llm.model_name == settings.OPENROUTER_MODEL


def test_llm_factory_invalid_provider():
    """Prueba el Fallback del Factory con un proveedor inválido."""
    with patch.object(settings, "LLM_PROVIDER", "INVALIDO"):
        with pytest.raises(ValueError, match="Proveedor no soportado"):
            get_llm()


def test_llm_factory_all_providers(monkeypatch):
    """Prueba todas las ramas del Factory (OpenAI, Google, Groq)."""

    # 1. Inyectamos API Keys falsas en el entorno para evitar que los SDKs fallen
    monkeypatch.setenv("OPENAI_API_KEY", "fake-openai-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-google-key")
    monkeypatch.setenv("GROQ_API_KEY", "fake-groq-key")

    # 2. Cubre líneas 23-26 (OPENAI)
    with patch.object(settings, "LLM_PROVIDER", "OPENAI"):
        llm = get_llm()
        assert llm.model_name == settings.OPENAI_MODEL

    # 3. Cubre líneas 29-32 (GOOGLE)
    with patch.object(settings, "LLM_PROVIDER", "GOOGLE"):
        llm = get_llm()
        assert llm.model == settings.GOOGLE_MODEL

    # 4. Cubre líneas 35-38 (GROQ)
    with patch.object(settings, "LLM_PROVIDER", "GROQ"):
        llm = get_llm()
        assert llm.model_name == settings.GROQ_MODEL


@patch("app.main.agent_app.ainvoke")
def test_chat_endpoint_internal_error(mock_ainvoke):
    """Cubre el bloque except Exception en main.py (líneas 64-65)."""
    mock_ainvoke.side_effect = Exception("Fallo simulado para cobertura")

    response = client.post("/chat", data={"query": "Hola"})

    assert response.status_code == 500
    assert "Error interno del agente" in response.json()["detail"]
