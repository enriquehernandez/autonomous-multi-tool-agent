import httpx
from langchain_core.tools import tool


@tool
def get_weather(latitude: float, longitude: float) -> str:
    """
    Obtiene el clima actual para una ubicación geográfica.
    Usa la API gratuita de Open-Meteo (no requiere API Key).

    Args:
        latitude: Latitud de la ubicación (ej. -33.45 para Santiago de Chile)
        longitude: Longitud de la ubicación (ej. -70.66 para Santiago de Chile)

    Returns:
        Un string con la temperatura actual y la velocidad del viento, o un mensaje de error controlado.
    """
    try:
        # Open-Meteo API: gratuita, sin autenticación
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}&current_weather=true"
        )

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        current = data.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")

        if temp is None:
            return "No se pudo obtener la información del clima para esa ubicación."

        return f"Clima actual: {temp}°C, viento a {wind} km/h (lat: {latitude}, lon: {longitude})."

    except httpx.TimeoutException:
        return "Error: El servicio del clima no respondió a tiempo. Intenta nuevamente."
    except httpx.HTTPStatusError as e:
        return f"Error del servicio del clima (código {e.response.status_code}). Intenta más tarde."
    except Exception as e:
        return f"Error inesperado al consultar el clima: {str(e)}"
