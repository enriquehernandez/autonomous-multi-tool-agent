import httpx
from langchain_core.tools import tool


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
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es&format=json"

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        results = data.get("results")
        if not results:
            return f"No se encontraron coordenadas para la ciudad: {city}."

        lat = results[0].get("latitude")
        lon = results[0].get("longitude")
        name = results[0].get("name")
        country = results[0].get("country")

        return f"Las coordenadas de {name}, {country} son: latitud {lat}, longitud {lon}."

    except Exception as e:
        return f"Error al buscar coordenadas de {city}: {str(e)}"
