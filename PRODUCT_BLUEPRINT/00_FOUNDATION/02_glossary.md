# Glosario Técnico de Agentes e IA

### ¿Qué es un Agente Autónomo?
Es un sistema de IA que no solo responde preguntas, sino que **razona** sobre ellas y **decide** qué acciones tomar (usar herramientas, buscar información, etc.) para cumplir un objetivo.

### ¿Qué es LangGraph?
Es un framework de LangChain para construir agentes como **grafos de estados**. A diferencia de una cadena lineal, permite ciclos (el agente piensa → actúa → observa → vuelve a pensar), lo que habilita el razonamiento iterativo.

### ¿Qué es Tool Calling (Function Calling)?
Es la capacidad del LLM de devolver una estructura JSON que indica "necesito ejecutar esta función con estos parámetros". El orquestador (LangGraph) ejecuta la función y le devuelve el resultado al LLM para que continúe razonando.

### ¿Qué es ReAct?
Es un patrón de prompting que combina **Reason** (razonamiento) y **Act** (acción). El agente primero razona sobre qué hacer, luego actúa (usa una herramienta), observa el resultado y repite el ciclo hasta tener una respuesta final.

### ¿Qué es Multimodalidad?
Es la capacidad de un modelo de IA de procesar múltiples tipos de entrada: texto, imágenes, audio, etc. En este proyecto, el agente puede recibir una imagen (ej. ticket) y extraer información de ella.

### ¿Qué es un Fallback?
Es una estrategia de resiliencia: si una acción falla (ej. una API externa no responde), el sistema no se rompe, sino que ejecuta una alternativa controlada (informar al usuario, usar otro proveedor, etc.).

### ¿Qué es el AgentState?
Es el objeto que persiste durante toda la ejecución del grafo. Contiene la lista de mensajes (Humano, AI, Tool) y permite que el agente tenga memoria de lo que ha hecho.

### ¿Qué es Tool Chaining (Encadenamiento de Herramientas)?
Es la capacidad de un agente de usar el resultado de una herramienta como entrada para otra. Por ejemplo, primero usa una API de geocodificación para obtener la latitud/longitud de Miami, y luego usa esos datos en la API del clima. Esto permite resolver problemas complejos en múltiples pasos.