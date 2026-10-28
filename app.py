import os, json, urllib.request, urllib.error
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
API_URL = "https://api.openai.com/v1/responses"
MAX_BODY = 100_000

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/api/health")
def health():
    return jsonify(ok=True, key_configured=bool(os.environ.get("OPENAI_API_KEY")))

@app.post("/api/respond")
def respond():
    expected = os.environ.get("APP_ACCESS_TOKEN", "").strip()
    supplied = request.headers.get("X-App-Token", "")
    if not expected:
        return jsonify(ok=False, error="El administrador aún no ha configurado el código de acceso."), 503
    if not supplied or not __import__("hmac").compare_digest(supplied, expected):
        return jsonify(ok=False, error="Código de acceso incorrecto."), 401
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return jsonify(ok=False, error="El administrador aún no ha configurado la clave API."), 503
    if request.content_length and request.content_length > MAX_BODY:
        return jsonify(ok=False, error="Solicitud demasiado grande."), 413
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    model = str(data.get("model", "")).strip()
    if not prompt or len(prompt) > 20000:
        return jsonify(ok=False, error="El mensaje está vacío o supera 20 000 caracteres."), 400
    if not model or len(model) > 120:
        return jsonify(ok=False, error="Indica un modelo válido."), 400
    payload = json.dumps({"model": model, "input": prompt, "store": False}).encode()
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        texts = []
        for item in result.get("output", []):
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text" and content.get("text"):
                        texts.append(content["text"])
        return jsonify(ok=True, text="\n".join(texts).strip(), response_id=result.get("id"))
    except urllib.error.HTTPError as e:
        try:
            obj = json.loads(e.read().decode("utf-8", errors="replace"))
            msg = obj.get("error", {}).get("message", "La API rechazó la solicitud.")
        except Exception:
            msg = "La API rechazó la solicitud (HTTP %s)." % e.code
        return jsonify(ok=False, error=("Error de API: " + str(msg))[:700]), 502
    except urllib.error.URLError as e:
        return jsonify(ok=False, error="No se pudo conectar con la API: " + str(e.reason)), 502
    except Exception as e:
        app.logger.exception("Error en /api/respond")
        return jsonify(ok=False, error=("Error interno: " + str(e))[:300]), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
