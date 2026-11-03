import httpx
from langchain_core.tools import tool
from app.core.config import settings


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convierte un monto de una moneda a otra usando tipos de cambio actuales.
    USA ESTA HERRAMIENTA SIEMPRE que el usuario pida convertir un monto entre monedas,
    o cuando hayas extraído un monto de una imagen y necesites su equivalente en otra moneda.
    """
    try:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()

        # --- LÓGICA DE SELECCIÓN DE PROVEEDOR ---
        if settings.EXCHANGE_RATE_API_KEY:
            # Opción A: Usar ExchangeRate-API (Requiere Key, más datos)
            url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/{from_curr}"
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            if data.get("result") != "success":
                return f"Error: No se pudo obtener el tipo de cambio para {from_curr} (Proveedor: ExchangeRate-API)."

            rate = data.get("conversion_rates", {}).get(to_curr)
        else:
            # Opción B: Usar Frankfurter (Gratis, sin Key)
            url = f"{settings.CURRENCY_API_URL}?base={from_curr}"
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()

            # Frankfurter v2 devuelve una lista
            rate = None
            for item in data:
                if item.get("quote") == to_curr:
                    rate = item.get("rate")
                    break

        if rate is None:
            return f"Error: La moneda de destino {to_curr} no está soportada o no se encontró tasa."

        converted_amount = amount * rate
        provider_name = "ExchangeRate-API" if settings.EXCHANGE_RATE_API_KEY else "Frankfurter"

        return f"{amount:,.2f} {from_curr} equivale a {converted_amount:,.2f} {to_curr} (Tasa: 1 {from_curr} = {rate:.4f} {to_curr}). Fuente: {provider_name}."

    except httpx.TimeoutException:
        return "Error: El servicio de conversión de divisas no respondió a tiempo. Intenta nuevamente."
    except httpx.HTTPStatusError as e:
        return f"Error del servicio de divisas (código {e.response.status_code}). Intenta más tarde."
    except Exception as e:
        return f"Error inesperado al convertir divisas: {str(e)}"
