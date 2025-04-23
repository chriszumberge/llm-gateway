from flask import Flask, jsonify
from gateway.routes import router
from httpx import HTTPStatusError

def create_app():
    app = Flask(__name__)
    # You can load config here, e.g. app.config.from_envvar(...)

    # --- Error handler for upstream HTTP errors (OpenAI, etc.) ---
    @app.errorhandler(HTTPStatusError)
    def handle_httpx_error(exc: HTTPStatusError):
        # Try to parse a JSON error from the provider
        try:
            payload = exc.response.json()  # e.g. {"error": {...}}
            err = payload.get("error", {})
            message = err.get("message") or err.get("detail") or str(exc)
            code    = err.get("type") or err.get("code") or ""
        except Exception:
            message = str(exc)
            code    = ""

        return jsonify({
            "error": {
                "code": code,
                "message": message
            }
        }), exc.response.status_code

    # Optionally catch *any* exception to return JSON
    @app.errorhandler(Exception)
    def handle_all_errors(exc):
        # If it's not an HTTPStatusError, wrap generically
        return jsonify({
            "error": {
                "code": "internal_error",
                "message": str(exc)
            }
        }), 500

    app.register_blueprint(router, url_prefix="")
    return app

def main():
    app = create_app()
    # Turn off the interactive debugger PIN prompt
    app.run(host="0.0.0.0", port=8000, debug=False)

if __name__ == "__main__":
    main() 