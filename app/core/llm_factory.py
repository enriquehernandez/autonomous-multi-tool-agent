# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# from app.core.config import settings


# def get_llm():
#     """
#     Factory Pattern: Retorna una instancia del LLM según la variable LLM_PROVIDER.
#     Todos los modelos seleccionados deben soportar Vision y Tool Calling.
#     """
#     provider = settings.LLM_PROVIDER.upper()
#     print(f"🤖 [LLM FACTORY] Inicializando proveedor: {provider}")

#     if provider == "OPENROUTER":
#         return ChatOpenAI(
#             model=settings.OPENROUTER_MODEL,
#             api_key=settings.OPENROUTER_API_KEY,
#             base_url="https://openrouter.ai/api/v1",
#             temperature=0,
#         )
#     elif provider == "OPENAI":
#         return ChatOpenAI(
#             model=settings.OPENAI_MODEL,
#             api_key=settings.OPENAI_API_KEY,
#             temperature=0,
#         )
#     elif provider == "GOOGLE":
#         return ChatGoogleGenerativeAI(
#             model=settings.GOOGLE_MODEL,
#             google_api_key=settings.GOOGLE_API_KEY,
#             temperature=0,
#         )
#     elif provider == "GROQ":
#         return ChatGroq(
#             model=settings.GROQ_MODEL,
#             api_key=settings.GROQ_API_KEY,
#             temperature=0,
#         )
#     else:
#         raise ValueError(
#             f"Proveedor no soportado: {provider}. Usa OPENROUTER, OPENAI, GOOGLE o GROQ.")


from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.core.config import settings


def _build_openrouter() -> BaseChatModel:
    return ChatOpenAI(
        model=settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )


def _build_openai() -> BaseChatModel:
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )


def _build_google() -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=settings.GOOGLE_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )


def _build_groq() -> BaseChatModel:
    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
    )


# REGISTRY PATTERN: Diccionario que mapea el string del proveedor a su función constructora
_PROVIDER_REGISTRY: dict[str, Callable[[], BaseChatModel]] = {
    "OPENROUTER": _build_openrouter,
    "OPENAI": _build_openai,
    "GOOGLE": _build_google,
    "GROQ": _build_groq,
}


def get_llm() -> BaseChatModel:
    """
    Factory Pattern (Registry): Retorna una instancia del LLM según la variable LLM_PROVIDER.
    Todos los modelos seleccionados deben soportar Vision y Tool Calling.
    """
    provider = settings.LLM_PROVIDER.upper()
    print(f"🤖 [LLM FACTORY] Inicializando proveedor: {provider}")

    builder = _PROVIDER_REGISTRY.get(provider)

    if not builder:
        raise ValueError(
            f"Proveedor no soportado: {provider}. Usa OPENROUTER, OPENAI, GOOGLE o GROQ."
        )

    return builder()
