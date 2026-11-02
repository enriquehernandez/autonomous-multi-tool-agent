"""
Script CLI para probar el agente sin necesidad de levantar FastAPI.
Uso: uv run python scripts/test_agent.py
"""
import asyncio
from langchain_core.messages import HumanMessage
from app.services.agent_engine import agent_app


async def main():
    print("🤖 Agente Autónomo listo. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() in ("salir", "exit", "quit"):
            print("👋 ¡Hasta luego!")
            break
        if not user_input:
            continue

        inputs = {"messages": [HumanMessage(content=user_input)]}
        result = await agent_app.ainvoke(inputs)

        # Mostrar pasos intermedios (razonamiento del agente)
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print(
                    f"  🛠️  [Herramienta solicitada: {[tc['name'] for tc in msg.tool_calls]}]")

        final_response = result["messages"][-1].content
        print(f"\n🤖 Agente: {final_response}\n")


if __name__ == "__main__":
    asyncio.run(main())
