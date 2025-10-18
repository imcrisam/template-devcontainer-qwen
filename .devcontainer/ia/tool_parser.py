from fastapi import FastAPI, Request
import httpx
import uvicorn

app = FastAPI()

# La URL interna de tu llama-server
LLAMA_SERVER_URL = "http://localhost:8080/v1/completions"  # ajusta según tu endpoint real

@app.post("/chat/completions")
async def proxy_to_ia(req: Request):
    body = await req.json()
    print("Incoming request to proxy:", body)
    async with httpx.AsyncClient() as client:
        resp = await client.post(LLAMA_SERVER_URL, json=body)
    print("Response from IA:", resp.json())
    return resp.json()

@app.post("/{full_path:path}")
async def catch_all_post(full_path: str, req: Request):
    body = await req.json()
    print(f"POST request to /{full_path}:")
    print(body)
    return {"status": "received", "path": full_path, "body": body}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)  # puerto expuesto para el contenedor
