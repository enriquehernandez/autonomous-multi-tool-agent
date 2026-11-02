import httpx
from langchain_core.tools import tool


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convierte un monto de una moneda a otra usando tipos de cambio actuales.
    USA ESTA HERRAMIENTA SIEMPRE que el usuario pida convertir un monto entre monedas,
    o cuando hayas extraído un monto de una imagen y necesites su equivalente en otra moneda.

    Args:
        amount: El monto a convertir (ej. 27000.0)
        from_currency: Código ISO de la moneda de origen (ej. 'USD', 'EUR', 'CLP')
        to_currency: Código ISO de la moneda de destino (ej. 'USD', 'EUR', 'CLP')

    Returns:
        Un string con el resultado de la conversión o un mensaje de error controlado.
    """
    try:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()

        # Usamos open.er-api.com (Gratis, sin API Key, soporta CLP)
        url = f"https://open.er-api.com/v6/latest/{from_curr}"

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        # Verificar si la API devolvió éxito
        if data.get("result") != "success":
            return f"Error: No se pudo obtener el tipo de cambio para {from_curr}."

        rates = data.get("rates", {})

        if to_curr not in rates:
            return f"Error: La moneda de destino {to_curr} no está soportada por el servicio."

        # Calcular la conversión
        rate = rates[to_curr]
        converted_amount = amount * rate

        return f"{amount:,.2f} {from_curr} equivale a {converted_amount:,.2f} {to_curr} (Tasa de cambio: 1 {from_curr} = {rate:.4f} {to_curr})."

    except httpx.TimeoutException:
        return "Error: El servicio de conversión de divisas no respondió a tiempo. Intenta nuevamente."
    except httpx.HTTPStatusError as e:
        return f"Error del servicio de divisas (código {e.response.status_code}). Intenta más tarde."
    except Exception as e:
        return f"Error inesperado al convertir divisas: {str(e)}"
