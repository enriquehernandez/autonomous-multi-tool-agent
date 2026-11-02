# Fallback & Error Handling Strategy

La oferta de Coderio exige "controles de calidad y estrategias de fallbacks". En este proyecto se implementa de la siguiente forma:

## 1. Fallback a nivel de API Externa (Tools)
Si la API del clima o de divisas falla (Error 500, Timeout), la Tool captura la excepción y retorna un string controlado:
*"Error: No se pudo conectar con el servicio de clima. Intenta más tarde."*
El Agente recibe este mensaje, lo procesa y le informa al usuario de forma elegante, sin arrojar un Error 500 en la API principal de FastAPI.

## 2. Fallback a nivel de Modelo LLM
En el `llm_factory.py`, si el proveedor principal (ej. OpenRouter) falla o da error 429 (Rate Limit), el sistema puede conmutar automáticamente al proveedor secundario (ej. Groq o Gemini) si están configuradas sus API Keys.

## 3. Guardrails (Controles de Calidad)
El System Prompt incluye instrucciones de seguridad:
*"No inventes montos o datos. Si la imagen no es clara, pide al usuario que la vuelva a subir."*

## 4. Límite de Iteraciones
El grafo de LangGraph tiene un límite máximo de pasos para evitar bucles infinitos que consuman tokens innecesariamente.