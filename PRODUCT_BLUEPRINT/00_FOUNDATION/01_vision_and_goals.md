# Vision and Goals

## Visión
Crear una API REST de nivel producción que sirva como motor de agentes autónomos para empresas que necesiten automatizar tareas que involucren APIs externas, razonamiento y procesamiento multimodal.

## Objetivos Técnicos (Goals)
1. **Autonomía (ReAct):** Implementar un ciclo de razonamiento donde el LLM decide cuándo y qué herramienta usar.
2. **Flexibilidad (Provider-Agnostic):** Desacoplar la lógica del agente del proveedor de IA (Patrón Factory).
3. **Multimodalidad:** Permitir que el agente procese imágenes junto con texto para extraer información estructurada.
4. **Resiliencia:** Manejar errores de red y límites de tasa (Rate Limits) sin romper la experiencia del usuario.
5. **Auditabilidad:** Devolver las herramientas usadas y el número de pasos ejecutados para trazabilidad.