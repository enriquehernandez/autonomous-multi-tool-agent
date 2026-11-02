# Architecture Design - LangGraph Agent

## 1. Flujo del Grafo (State Machine)
A diferencia de una cadena lineal (LCEL), el agente usa un grafo con ciclos.

```mermaid
graph TD
    A[Usuario (Texto + Imagen)] --> B(Nodo: Agente LLM)
    B -->|¿Necesita herramienta?| C{Decisión}
    C -->|Sí| D(Nodo: Tool Calling)
    D -->|API REST Clima/Moneda| E[Servicios Externos]
    E -->|Resultado| B
    C -->|No| F[Respuesta Final al Usuario]
```

## 2. Componentes de Software

- Agent Engine (agent_engine.py): Orquestador construido con StateGraph de LangGraph.
- Tools (app/tools/): Funciones de Python decoradas con @tool que hacen peticiones HTTP usando httpx.
- LLM Factory: Configurable vía .env para usar GPT-4o (OpenAI) o Gemini 1.5 Pro (Google), ambos soportan Visión.