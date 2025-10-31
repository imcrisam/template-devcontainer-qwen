import os
import json
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
from flask import Flask, request, Response
import requests

# Config
# TARGET =  "https://openrouter.ai/api"
TARGET =  "http://ai:8080"
LOG_FILE = os.environ.get("PROXY_LOG_FILE", "proxy.log")
MAX_LOG_BYTES = int(os.environ.get("MAX_LOG_BYTES", 50_000_000))  # 50MB
BACKUP_COUNT = int(os.environ.get("LOG_BACKUPS", 3))

# Logger
logger = logging.getLogger("proxy")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")

# Consola
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(fmt)
logger.addHandler(ch)

# Archivo rotativo
fh = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
fh.setFormatter(fmt)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

app = Flask(__name__)


# Guarda fragmentos por id
_response_accumulator = defaultdict(str)

def parse_stream(resp):
    result = {
        "contents": [],
        "tools": defaultdict(lambda: {"arguments": ""})
    }
    logger.info("◀ [RESPONSE] Status: %s", resp.status_code)

    current_content = ""
    current_tool = None
    lines = resp.iter_lines()
    for raw in lines:
        # logger.debug(f"RAW LINE: {raw!r}")
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        raw = raw.strip()
        if not raw.startswith("data:"):
            continue

        try:
            payload = json.loads(raw[len("data:"):].strip())
        except json.JSONDecodeError:
            logger.warning(f"No se pudo decodificar: {raw[:100]}...")
            continue

        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            continue
        delta = choices[0].get("delta", {})
        if not delta:
            continue

        # Caso 1: contenido normal
        if "content" in delta:
            chunk = delta["content"]
            if isinstance(chunk, str):
                current_content += chunk
            continue

        # Caso 2: tool_call detectado
        tool_calls = delta.get("tool_calls", [])
        for call in tool_calls:
            fn = call.get("function", {})
            name = fn.get("name")
            args = fn.get("arguments", "")

            if name:
                current_tool = name
                result["tools"][current_tool]["name"] = name
                if current_content:
                    result["contents"].append(current_content.strip())
                    current_content = ""

            if current_tool and args:
                result["tools"][current_tool]["arguments"] += args

    if current_content:
        result["contents"].append(current_content.strip())

    logger.info("=== Resultado parse_stream ===")
    logger.info(json.dumps(result, indent=2, ensure_ascii=False))

    return result



# Helpers
def _pretty_json_or_text(data: bytes) -> str:
    if not data:
        return "<empty>"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return f"<binary {len(data)} bytes>"
    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return text.strip()

LOG_EXCLUDE_KEYS = ["tools"]
def _log_request(body, req):
    _response_accumulator = defaultdict(str)
    logger.info("▶ [REQUEST] %s %s%s", req.method, req.path, f"?{req.query_string.decode()}" if req.query_string else "")
    logger.debug("- Headers:\n%s", json.dumps(dict(req.headers), indent=2, ensure_ascii=False))
        # Si el body es JSON, eliminamos las claves excluidas antes de imprimir
    try:
        body_json = json.loads(body)
        if isinstance(body_json, dict):
            for key in LOG_EXCLUDE_KEYS:
                body_json.pop(key, None)
            body_to_log = json.dumps(body_json, indent=2, ensure_ascii=False)
        else:
            body_to_log = _pretty_json_or_text(body)
    except Exception:
        body_to_log = _pretty_json_or_text(body)

    logger.debug("- Body:\n%s\n%s", body_to_log, "-" * 80)

def _log_response(resp):
    logger.info("◀ [RESPONSE] Status: %s", resp.status_code)
    logger.debug("- Headers:\n%s", json.dumps(dict(resp.headers), indent=2, ensure_ascii=False))
    logger.debug("- Body:\n%s\n%s", _pretty_json_or_text(resp.content), "=" * 80)

def _add_tool_choice_to_body(body: bytes) -> bytes:
    try:
        data = json.loads(body)
        if isinstance(data, dict) and "tool_choice" not in data:
            data["tool_choice"] = "required"
            return json.dumps(data).encode("utf-8")
    except Exception:
        pass
    return body

# Proxy handler
@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def proxy(path):
    _log_request(request.get_data(), request)

    upstream = f"{TARGET.rstrip('/')}/{path}"
    excluded_headers = {
        "host", "content-length", "transfer-encoding", "connection", "keep-alive",
        "proxy-authenticate", "proxy-authorization", "te", "trailer", "upgrade"
    }
    headers = {k: v for k, v in request.headers if k.lower() not in excluded_headers}
    modified_data = _add_tool_choice_to_body(request.get_data())
    # _log_request(modified_data, request)
    try:
        resp = requests.request(
            method=request.method,
            url=upstream,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=float(os.environ.get("UPSTREAM_TIMEOUT", "30")),
        )
    except requests.RequestException as e:
        logger.exception("❌ Error talking to upstream: %s", e)
        return Response(f"Upstream request failed: {e}", status=502)

    # _log_response(resp)
    parse_stream(resp)
    excluded_resp_headers = {"content-encoding", "transfer-encoding", "connection", "keep-alive"}
    response_headers = [(n, v) for n, v in resp.headers.items() if n.lower() not in excluded_resp_headers]

    return Response(resp.content, status=resp.status_code, headers=response_headers)

if __name__ == "__main__":
    host = os.environ.get("PROXY_HOST", "0.0.0.0")
    port = int(os.environ.get("PROXY_PORT", 8080))
    logger.info("🚀 Proxy listening on %s:%s → %s", host, port, TARGET)
    app.run(host=host, port=port)
