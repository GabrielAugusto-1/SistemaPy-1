from flask import Flask
from routes import clientes_bp

app = Flask(__name__)

app.register_blueprint(clientes_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
