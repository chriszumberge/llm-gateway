from flask import Flask
from gateway.routes import router

def create_app():
    app = Flask(__name__)
    # You can load config here, e.g. app.config.from_envvar(...)
    app.register_blueprint(router, url_prefix="")
    return app

def main():
    app = create_app()
    # In production, you'll use a WSGI server instead of Flask.run
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == "__main__":
    main() 