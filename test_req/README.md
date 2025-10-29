# 📁 Directorio test_req
Este directorio contiene los archivos necesarios para ejecutar pruebas y configuraciones relacionadas con el ambiente IA.
## Archivos del proyecto:
- `agent.http` - Plantilla de chat utilizada por agentes AI locales. Se usa como base para llamados a modelos mediante herramientas en entornos DevContainer
  
- `chat.http` – Contiene configuraciones y plantillas relacionadas con el sistema.

- `json.json` – Archivo JSON que contiene mensajes estructurados, normalmente usado por agentes IA locales como parte de sus interacciones (por ejemplo: herramientas).

- `props.http`	– Define propiedades del servidor para pruebas y configuraciones específicas. Se usa principalmente en entornos DevContainer.
  
## Ejemplo:
```http
# POST http://ia:8080/chat/completions
POST http://ia:8080/v1/chat/completions
Content-Type: application/json
{
    "model": "Qwen3-Coder-30B-A3B-Instruct",
  	"messages":[{"role":"system","content":"You are a systematic coding agent. Break down problems methodically."},{"role":"user", "content":"explicame el readme"}],   
	"max_tokens":4096,
    "stream":true
}
```	  