from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage, HumanMessage
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
    system_prompt = """Eres un asistente financiero autónomo. 
    Tu objetivo es ayudar al usuario usando las herramientas disponibles.
    Si el usuario te envía una imagen de un ticket, extrae el monto y usa la herramienta de conversión de moneda.
    Si una herramienta falla, informa al usuario elegantemente."""

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

agent_app = workflow.compile()
