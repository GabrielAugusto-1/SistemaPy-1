from flask import Blueprint, jsonify
from services import ClienteService

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes" )

@clientes_bp.route("/", methods=["GET"])
def mostrar_cliente():
    cliente = ClienteService.listar_cliente_ativos()
    return cliente, 200

@clientes_bp.route("/", methods=["POST"])
def criar_cliente():
    