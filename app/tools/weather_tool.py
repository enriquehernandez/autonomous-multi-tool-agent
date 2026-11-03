import httpx
from langchain_core.tools import tool
from app.core.config import settings


@tool
def get_weather(latitude: float, longitude: float, city: str = "") -> str:
    """
    Obtiene el clima actual para una ubicación geográfica.
    Args:
        latitude: Latitud (ej. -33.45)
        longitude: Longitud (ej. -70.66)
        city: Nombre de la ciudad (opcional, solo necesario si se usa OpenWeatherMap)
    """
    try:
        # --- LÓGICA DE SELECCIÓN DE PROVEEDOR ---
        if settings.WEATHER_API_KEY:
            # Opción A: Usar OpenWeatherMap (Requiere Key)
            # Si el agente no pasó la ciudad, usamos las coordenadas
            if city:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WEATHER_API_KEY}&units=metric"
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.WEATHER_API_KEY}&units=metric"

            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            temp = data.get("main", {}).get("temp")
            wind = data.get("wind", {}).get("speed")
            return f"Clima actual (OpenWeatherMap): {temp}°C, viento a {wind} m/s."

        else:
            # Opción B: Usar Open-Meteo (Gratis, sin Key)
            url = (
                f"{settings.WEATHER_API_URL}"
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

            return f"Clima actual (Open-Meteo): {temp}°C, viento a {wind} km/h (lat: {latitude}, lon: {longitude})."

    except httpx.TimeoutException:
        return "Error: El servicio del clima no respondió a tiempo. Intenta nuevamente."
    except httpx.HTTPStatusError as e:
        return f"Error del servicio del clima (código {e.response.status_code}). Intenta más tarde."
    except Exception as e:
        return f"Error inesperado al consultar el clima: {str(e)}"
