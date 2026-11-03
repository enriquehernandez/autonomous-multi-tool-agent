import pytest
import operator
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
import app.services.agent_engine as engine


def test_agent_state_accumulates_messages():
    state_1 = {"messages": [HumanMessage(content="Hola")]}
    state_2 = {"messages": operator.add(
        state_1["messages"], [AIMessage(content="¿En qué te ayudo?")])}
    assert len(state_2["messages"]) == 2
    assert state_2["messages"][0].content == "Hola"


@pytest.mark.asyncio
async def test_agent_flow_state_transitions(monkeypatch):
    msg_tool_call = AIMessage(
        content="",
        tool_calls=[{"name": "convert_currency", "args": {
            "amount": 100, "from_currency": "USD", "to_currency": "CLP"}, "id": "call_123"}]
    )
    msg_final = AIMessage(content="100 USD son 95,000 CLP.")

    respuestas = [msg_tool_call, msg_final]
    contador = {"i": 0}

    def fake_llm_call(inputs):
        res = respuestas[contador["i"]]
        contador["i"] += 1
        return res

    fake_runnable = RunnableLambda(fake_llm_call)
    fake_runnable.bind_tools = lambda tools, **kwargs: fake_runnable
    monkeypatch.setattr(engine, "llm_with_tools", fake_runnable)

    def mock_convert_currency(amount, from_currency, to_currency):
        return f"{amount} {from_currency} equivale a 95000 CLP."

    for tool in engine.tools:
        if tool.name == "convert_currency":
            monkeypatch.setattr(tool, "func", mock_convert_currency)
            break

    workflow = StateGraph(engine.AgentState)
    workflow.add_node("agent", engine.call_model)
    workflow.add_node("tools", engine.tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", engine.should_continue)
    workflow.add_edge("tools", "agent")
    test_app = workflow.compile()

    inputs = {"messages": [HumanMessage(content="Convierte 100 USD a CLP")]}
    result = await test_app.ainvoke(inputs)

    messages = result["messages"]
    assert len(messages) == 4
    assert isinstance(messages[2], ToolMessage)
    assert "95,000 CLP" in messages[3].content
