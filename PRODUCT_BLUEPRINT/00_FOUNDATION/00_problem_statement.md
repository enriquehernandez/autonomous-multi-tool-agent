# Problem Statement

## Contexto
Los LLMs tradicionales son "cajas negras" que solo generan texto basado en su entrenamiento. Sin embargo, en el mundo empresarial, un asistente debe poder **actuar** sobre sistemas externos (consultar saldos, convertir monedas, enviar correos) y **entender** múltiples formatos (como fotos de boletas o contratos escaneados).

## Solución Propuesta
Desarrollar un **Agente Autónomo** basado en LangGraph que:
1. **Razone (ReAct):** Decida por sí mismo qué acción tomar basándose en la pregunta del usuario.
2. **Use Herramientas (Tool Calling):** Se conecte a APIs REST externas de forma segura.
3. **Sea Multimodal:** Pueda recibir imágenes (ej. tickets de compra), extraer la información mediante un modelo de visión y luego usar una herramienta para procesar esos datos.
4. **Resiliente (Fallbacks):** Si una API externa falla, el agente no se rompe; busca alternativas o informa al usuario.