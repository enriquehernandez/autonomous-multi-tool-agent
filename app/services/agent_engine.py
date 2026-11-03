from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.llm_factory import get_llm
from app.tools import tools

# 1. Definimos el Estado (Memoria del agente)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


# 2. Configuramos el LLM con las herramientas
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)

# 3. Nodo del Agente (El cerebro que decide)


def call_model(state: AgentState):
    system_prompt = """Eres un asistente financiero autónomo y proactivo. 
    Tu objetivo es resolver la solicitud del usuario de principio a fin usando las herramientas disponibles.

    Reglas de comportamiento:
    1. **Prioridad de la Consulta:** Responde siempre a la pregunta de texto del usuario. 
    2. **Uso de Imágenes:** Si el usuario adjunta una imagen, SOLO úsala si el texto de la consulta hace referencia a ella o si es necesaria para responder la pregunta (ej. "convierte el monto de este ticket"). Si el texto pregunta por el clima y la imagen es un ticket, ignora la imagen y responde solo sobre el clima.
    3. **Autonomía:** Si el usuario te pide convertir un monto, USA LA HERRAMIENTA `convert_currency` INMEDIATAMENTE.
    4. **Clima:** Si el usuario pregunta por el clima de una ciudad, ESTIMA sus coordenadas (latitud y longitud) usando tu conocimiento general y usa `get_weather` inmediatamente. Por ejemplo, para Miami usa (25.76, -80.19). No le pidas al usuario las coordenadas.
    5. **Fallbacks:** Si una herramienta falla, informa al usuario elegantemente y sugiere alternativas.
    6. **Precisión:** No inventes datos. Si no puedes extraer el monto de la imagen, pide al usuario que la vuelva a subir.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = prompt | llm_with_tools
    response = chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}


# 4. Nodo de Herramientas
tool_node = ToolNode(tools)

# 5. Condición de salida (Si el LLM pidió usar una tool, vamos a la tool. Si no, terminamos)


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


# 6. Construimos el Grafo
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
# Después de usar la tool, vuelve al agente a razonar
workflow.add_edge("tools", "agent")

# 7. Configuración de ejecución con Fallback de iteraciones
agent_app = workflow.compile()
# Nota: Al invocar el agente, puedes limitar los pasos así:
# result = await agent_app.ainvoke(inputs, config={"recursion_limit": 5})
