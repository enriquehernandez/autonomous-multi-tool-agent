# Agent Graph Component

## Responsabilidad
Definir los nodos y aristas del agente, asegurando que el LLM tenga memoria y sepa cuándo detenerse.

## Contrato del Estado (AgentState)
```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
```
El estado acumula los mensajes (Humano, AI, Tool) en orden.

## Nodos
- agent: Invoca al LLM con el historial de mensajes. El LLM decide si responder directamente o solicitar una herramienta.
- tools: Ejecuta la herramienta solicitada y añade el resultado al estado.

## Aristas (Edges)
- agent -> tools (condicional): Si el LLM devuelve tool_calls, se ejecuta la herramienta.
- agent -> END (condicional): Si el LLM responde directamente, termina.
- tools -> agent: Después de ejecutar la herramienta, el agente vuelve a razonar con el resultado.

## Reglas de Negocio

1. `Límite de iteraciones`: El agente no puede dar más de 5 pasos (vueltas en el grafo) para evitar bucles infinitos y costos excesivos.
2. `Tool Calling`: El LLM debe devolver una estructura JSON válida al invocar una herramienta.
3. `Contexto Visual`: Si hay una imagen, el prompt del sistema debe instruir explícitamente al modelo a extraer los datos numéricos de la imagen antes de usar las tools.