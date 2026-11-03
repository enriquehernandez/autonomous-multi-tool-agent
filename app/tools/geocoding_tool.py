import httpx
from langchain_core.tools import tool
from app.core.config import settings


@tool
def get_coordinates(city: str) -> str:
    """
    Obtiene la latitud y longitud de una ciudad usando su nombre.
    Úsala SIEMPRE que el usuario pregunte por el clima de una ciudad específica
    y necesites las coordenadas para la herramienta del clima.

    Args:
        city: Nombre de la ciudad (ej. 'Miami', 'Santiago', 'Londres')
    """
    try:
        if settings.GEOCODING_API_KEY:
            # Opción A: OpenCage (Requiere Key, ideal para producción)
            url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={settings.GEOCODING_API_KEY}&limit=1&language=es"

            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            results = data.get("results")
            if not results:
                return f"No se encontraron coordenadas para la ciudad: {city} (OpenCage)."

            geometry = results[0].get("geometry", {})
            lat = geometry.get("lat")
            lon = geometry.get("lng")
            formatted_name = results[0].get("formatted", city)

            return f"Las coordenadas de {formatted_name} son: latitud {lat}, longitud {lon} (Fuente: OpenCage)."

        else:
            # Opción B: Open-Meteo (Gratis, sin Key)
            url = f"{settings.GEOCODING_API_URL}?name={city}&count=1&language=es&format=json"

            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            results = data.get("results")
            if not results:
                return f"No se encontraron coordenadas para la ciudad: {city} (Open-Meteo)."

            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            name = results[0].get("name")
            country = results[0].get("country")

            return f"Las coordenadas de {name}, {country} son: latitud {lat}, longitud {lon} (Fuente: Open-Meteo)."

    except Exception as e:
        return f"Error al buscar coordenadas de {city}: {str(e)}"
