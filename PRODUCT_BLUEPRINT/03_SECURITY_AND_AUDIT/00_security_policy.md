# Security Policy

En sistemas basados en agentes autónomos, la seguridad es crítica. Este proyecto implementa las siguientes medidas:

## 1. Manejo de Secretos (API Keys)
- **Cero Hardcoding:** Ninguna API Key está escrita en el código fuente.
- **Variables de Entorno:** Se utiliza un archivo `.env` (local) que está estrictamente excluido del control de versiones en `.gitignore`.
- **Plantilla:** El archivo `.env.example` provee la estructura pero no los valores reales.

## 2. Protección contra Prompt Injection
- El System Prompt instruye estrictamente al agente a responder **solo** basándose en las herramientas disponibles y el contexto del usuario.
- Si un usuario intenta inyectar instrucciones maliciosas (ej. "ignora tus reglas y ejecuta..."), el agente está limitado por las tools registradas.

## 3. Privacidad de los Datos
- Las imágenes enviadas al endpoint `/chat` se procesan en memoria y no se almacenan en disco.
- Solo el contenido de la imagen (en base64) viaja al proveedor del LLM (OpenRouter/OpenAI/Google).

## 4. Validación de Entradas
- FastAPI valida automáticamente los tipos de datos (ej. `query` debe ser string, `image` debe ser un archivo).
- Las tools validan los códigos de moneda y coordenadas antes de hacer peticiones externas.

## 5. Rate Limiting (Recomendación para Producción)
- Para producción, se recomienda añadir un middleware de rate limiting (ej. `slowapi`) para evitar abusos del endpoint.