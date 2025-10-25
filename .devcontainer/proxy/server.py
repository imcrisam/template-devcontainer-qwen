import os
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, Response
import requests

# Config
TARGET = os.environ.get("TARGET_URL", "https://httpbin.org")
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

def _log_request(req):
    body = req.get_data()
    logger.info("▶ [REQUEST] %s %s%s", req.method, req.path, f"?{req.query_string.decode()}" if req.query_string else "")
    logger.debug("- Headers:\n%s", json.dumps(dict(req.headers), indent=2, ensure_ascii=False))
    logger.debug("- Body:\n%s\n%s", _pretty_json_or_text(body), "-" * 80)

def _log_response(resp):
    logger.info("◀ [RESPONSE] Status: %s", resp.status_code)
    logger.debug("- Headers:\n%s", json.dumps(dict(resp.headers), indent=2, ensure_ascii=False))
    logger.debug("- Body:\n%s\n%s", _pretty_json_or_text(resp.content), "=" * 80)

# Proxy handler
@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def proxy(path):
    _log_request(request)

    upstream = f"{TARGET.rstrip('/')}/{path}"
    excluded_headers = {
        "host", "content-length", "transfer-encoding", "connection", "keep-alive",
        "proxy-authenticate", "proxy-authorization", "te", "trailer", "upgrade"
    }
    headers = {k: v for k, v in request.headers if k.lower() not in excluded_headers}

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

    _log_response(resp)

    excluded_resp_headers = {"content-encoding", "transfer-encoding", "connection", "keep-alive"}
    response_headers = [(n, v) for n, v in resp.headers.items() if n.lower() not in excluded_resp_headers]

    return Response(resp.content, status=resp.status_code, headers=response_headers)

if __name__ == "__main__":
    host = os.environ.get("PROXY_HOST", "0.0.0.0")
    port = int(os.environ.get("PROXY_PORT", 8080))
    logger.info("🚀 Proxy listening on %s:%s → %s", host, port, TARGET)
    app.run(host=host, port=port)
