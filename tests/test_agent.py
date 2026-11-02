import pytest
from app.tools.currency_tool import convert_currency
from app.tools.weather_tool import get_weather


def test_convert_currency_success():
    """Prueba que la tool de divisas responde correctamente."""
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "CLP" in result
    assert "Error" not in result


def test_convert_currency_invalid_currency():
    """Prueba el fallback con una moneda inexistente."""
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "XXX", "to_currency": "CLP"})
    assert "Error" in result


def test_get_weather_success():
    """Prueba que la tool del clima responde correctamente para Santiago."""
    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "°C" in result
    assert "Error" not in result
