from flask import Flask
from clientes import clientes_bp
from produtos import produtos_bp

app = Flask(__name__)

app.register_blueprint(clientes_bp)
app.register_blueprint(produtos_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
