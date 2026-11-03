# Architecture Design - LangGraph Agent

## 1. Flujo del Grafo (State Machine)
A diferencia de una cadena lineal (LCEL), el agente usa un grafo con ciclos.

```mermaid
graph TD
    A[Usuario: Texto + Imagen] --> B(Nodo: Agente LLM)
    B -->|¿Necesita herramienta?| C{Decisión}
    C -->|Sí| D(Nodo: Tool Calling)
    D -->|3 Opciones| E[Currency API / Weather API / Geocoding API]
    E -->|Resultado| B
    C -->|No| F[Respuesta Final al Usuario]
```

## 2. Flujo de una Consulta Multimodal

```mermaid
sequenceDiagram
    participant U as Usuario
    participant API as FastAPI
    participant A as Agente (LangGraph)
    participant V as Modelo Vision (OpenRouter)
    participant T as Tool (Divisas)
    participant F as Frankfurter API

    U->>API: POST /chat (imagen + "convierte a USD")
    API->>A: HumanMessage (texto + imagen base64)
    A->>V: Analiza imagen, extrae monto y moneda
    V-->>A: Tool Call: convert_currency(amount, from, to)
    A->>T: Ejecuta tool
    T->>F: GET /latest?from=...&to=...
    F-->>T: Tipo de cambio
    T-->>A: Resultado de conversión
    A->>V: Genera respuesta final con el resultado
    V-->>A: Respuesta en lenguaje natural
    A-->>API: Respuesta final + tools_used
    API-->>U: JSON con respuesta
```

## 3. Componentes de Software

- `API Layer`: FastAPI (endpoints asíncronos, soporte para form-data con archivos).
- `Agent Engine`: StateGraph de LangGraph con nodos agent y tools.
- `Tools`: Funciones decoradas con @tool que usan httpx para llamadas HTTP.
- `LLM Factory`: Configurable vía .env para usar OpenRouter, OpenAI, Google o Groq.

## 4. Patrones de Diseño Aplicados
- **Registry Pattern (LLM Factory):** Utilizado en `llm_factory.py`. En lugar de usar estructuras condicionales (`if/elif`) para instanciar el proveedor de IA, se utiliza un diccionario (`_PROVIDER_REGISTRY`) que mapea el nombre del proveedor (`OPENROUTER`, `OPENAI`, etc.) a su función constructora. Esto respeta el principio Open/Closed (SOLID), permitiendo agregar nuevos proveedores sin modificar la función principal `get_llm()`.
- **State Machine:** LangGraph modela el agente como un grafo de estados con transiciones condicionales.
- **Resilience Pattern:** Las tools capturan excepciones y retornan mensajes controlados en lugar de propagar errores.