import pytest
import httpx
from unittest.mock import patch, MagicMock
from app.tools.currency_tool import convert_currency
from app.tools.weather_tool import get_weather
from app.tools.geocoding_tool import get_coordinates

# --- TESTS DE DIVISAS ---


@patch("app.core.config.settings.EXCHANGE_RATE_API_KEY", None)
def test_convert_currency_success_free():
    """Prueba la conversión usando el proveedor gratuito (Frankfurter)."""
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "CLP" in result
    assert "Error" not in result


@patch("app.core.config.settings.EXCHANGE_RATE_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_convert_currency_success_commercial(mock_get):
    """Prueba la conversión usando el proveedor comercial (ExchangeRate-API)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": "success", "conversion_rates": {"CLP": 950.0}}
    mock_get.return_value = mock_response

    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "95,000.00 CLP" in result


def test_convert_currency_invalid_currency():
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "XXX", "to_currency": "CLP"})
    assert "Error" in result


@patch("httpx.Client.get")
def test_convert_currency_timeout(mock_get):
    mock_get.side_effect = httpx.TimeoutException("Timeout")
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "Error" in result
    assert "no respondió a tiempo" in result

# --- TESTS DE CLIMA ---


@patch("app.core.config.settings.WEATHER_API_KEY", None)
def test_get_weather_success_free():
    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "°C" in result
    assert "Error" not in result


@patch("app.core.config.settings.WEATHER_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_get_weather_success_commercial(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 25}, "wind": {"speed": 5}}
    mock_get.return_value = mock_response

    result = get_weather.invoke(
        {"latitude": -33.45, "longitude": -70.66, "city": "Santiago"})
    assert "25°C" in result
    assert "5 m/s" in result


@patch("httpx.Client.get")
def test_get_weather_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error 500", request=MagicMock(), response=MagicMock(status_code=500)
    )
    mock_get.return_value = mock_response
    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "código 500" in result

# --- TESTS DE GEOCODIFICACIÓN ---


@patch("app.core.config.settings.GEOCODING_API_KEY", None)
def test_get_coordinates_success_free():
    result = get_coordinates.invoke({"city": "Miami"})
    assert "latitud" in result
    assert "longitud" in result


@patch("app.core.config.settings.GEOCODING_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_get_coordinates_success_commercial(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": [
        {"geometry": {"lat": 25.76, "lng": -80.19}, "formatted": "Miami, FL"}]}
    mock_get.return_value = mock_response

    result = get_coordinates.invoke({"city": "Miami"})
    assert "25.76" in result


@patch("httpx.Client.get")
def test_get_coordinates_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_get.return_value = mock_response
    result = get_coordinates.invoke({"city": "CiudadInventada123"})
    assert "No se encontraron coordenadas" in result


@patch("httpx.Client.get")
def test_get_coordinates_exception(mock_get):
    mock_get.side_effect = Exception("Error inesperado")
    result = get_coordinates.invoke({"city": "Miami"})
    assert "Error al buscar" in result


@patch("app.core.config.settings.EXCHANGE_RATE_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_convert_currency_commercial_error_response(mock_get):
    """Cubre la línea 27 (result != success de ExchangeRate-API)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "error"}
    mock_get.return_value = mock_response

    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "Error: No se pudo obtener el tipo de cambio" in result


@patch("app.core.config.settings.EXCHANGE_RATE_API_KEY", None)
@patch("httpx.Client.get")
def test_convert_currency_rate_not_found(mock_get):
    """Cubre la línea 46 (rate es None en Frankfurter)."""
    mock_response = MagicMock()
    # Simula que Frankfurter devuelve una lista vacía o sin la moneda buscada
    mock_response.json.return_value = [{"quote": "EUR", "rate": 1.0}]
    mock_get.return_value = mock_response

    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "GBP"})
    assert "no está soportada o no se encontró tasa" in result


@patch("httpx.Client.get")
def test_convert_currency_generic_exception(mock_get):
    """Cubre las líneas 57-58 (Exception genérica)."""
    mock_get.side_effect = ValueError("Error genérico simulado")
    result = convert_currency.invoke(
        {"amount": 100.0, "from_currency": "USD", "to_currency": "CLP"})
    assert "Error inesperado al convertir divisas" in result


@patch("app.core.config.settings.GEOCODING_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_get_coordinates_commercial_not_found(mock_get):
    """Cubre la línea 28 (OpenCage no encuentra resultados)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_get.return_value = mock_response

    result = get_coordinates.invoke({"city": "CiudadFalsa"})
    assert "No se encontraron coordenadas para la ciudad" in result


@patch("app.core.config.settings.WEATHER_API_KEY", "fake_key")
@patch("httpx.Client.get")
def test_get_weather_commercial_no_city(mock_get):
    """Cubre la línea 23 (OpenWeatherMap sin ciudad)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "main": {"temp": 20}, "wind": {"speed": 10}}
    mock_get.return_value = mock_response

    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "20°C" in result
    # Verifica que la URL usada fue la de lat/lon
    called_url = mock_get.call_args[0][0]
    assert "lat=" in called_url


@patch("app.core.config.settings.WEATHER_API_KEY", None)
@patch("httpx.Client.get")
def test_get_weather_free_no_data(mock_get):
    """Cubre la línea 51 (Open-Meteo no devuelve temp)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current_weather": {}}  # Sin "temperature"
    mock_get.return_value = mock_response

    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "No se pudo obtener la información del clima" in result


@patch("httpx.Client.get")
def test_get_weather_timeout(mock_get):
    """Cubre la línea 56 (Timeout)."""
    mock_get.side_effect = httpx.TimeoutException("Timeout")
    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "no respondió a tiempo" in result


@patch("httpx.Client.get")
def test_get_weather_generic_exception(mock_get):
    """Cubre la línea 60 (Exception genérica)."""
    mock_get.side_effect = ValueError("Error genérico simulado")
    result = get_weather.invoke({"latitude": -33.45, "longitude": -70.66})
    assert "Error inesperado al consultar el clima" in result
