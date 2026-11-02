# Tools Contract

## Responsabilidad
Definir el contrato de cada herramienta que el agente puede invocar.

## Tool: `convert_currency`
- **Descripción:** Convierte un monto entre dos monedas usando tipos de cambio oficiales.
- **Parámetros:**
  - `amount` (float): Monto a convertir.
  - `from_currency` (str): Código ISO de la moneda origen (ej. "USD").
  - `to_currency` (str): Código ISO de la moneda destino (ej. "CLP").
- **API Externa:** Frankfurter (`https://api.frankfurter.app`), gratuita, sin autenticación.
- **Retorno:** String con el resultado o mensaje de error controlado.

## Tool: `get_weather`
- **Descripción:** Obtiene el clima actual para una ubicación geográfica.
- **Parámetros:**
  - `latitude` (float): Latitud de la ubicación.
  - `longitude` (float): Longitud de la ubicación.
- **API Externa:** Open-Meteo (`https://api.open-meteo.com`), gratuita, sin autenticación.
- **Retorno:** String con temperatura y viento, o mensaje de error controlado.

## Reglas de Negocio
1. **Nunca lanzar excepciones no controladas:** Todas las tools deben capturar `httpx.TimeoutException`, `httpx.HTTPStatusError` y `Exception` genéricas.
2. **Mensajes de error legibles:** El agente debe poder entender el error y comunicarlo al usuario de forma natural.
3. **Idempotencia:** Las tools de solo lectura (clima, divisas) pueden llamarse múltiples veces sin efectos secundarios.