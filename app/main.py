from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
import base64
from langchain_core.messages import HumanMessage
from app.services.agent_engine import agent_app
from app.core.config import settings

app = FastAPI(
    title="Autonomous Multi-Tool Agent API",
    description="Agente autónomo con LangGraph, Tool Calling y capacidades multimodales.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Autonomous Multi-Tool Agent API",
        "provider": settings.LLM_PROVIDER,
        "model": settings.OPENROUTER_MODEL if settings.LLM_PROVIDER == "OPENROUTER" else "ver .env",
        "docs": "/docs",
    }


@app.post("/chat")
async def chat_with_agent(
    query: str = Form(...,
                      description="Pregunta o instrucción para el agente"),
    image: Optional[UploadFile] = File(
        None, description="Imagen opcional (ej. ticket, factura)"),
):
    try:
        content = [{"type": "text", "text": query}]

        # Si el usuario sube una imagen (Multimodalidad)
        if image:
            image_bytes = await image.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{image.content_type};base64,{image_b64}"},
            })

        inputs = {"messages": [HumanMessage(content=content)]}

        # Ejecutamos el grafo del agente
        result = await agent_app.ainvoke(inputs)

        # Extraemos la respuesta final
        final_response = result["messages"][-1].content

        # Extraemos las herramientas usadas (para auditoría)
        tools_used = [
            msg.name for msg in result["messages"]
            if hasattr(msg, "name") and msg.name
        ]

        return {
            "response": final_response,
            "steps_taken": len(result["messages"]),
            "tools_used": tools_used,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del agente: {str(e)}")
