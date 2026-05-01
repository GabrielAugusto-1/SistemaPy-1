from flask import Blueprint, jsonify, request
from services import ClienteService
from schema import ClienteCreateSchema

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes" )

@clientes_bp.route("/", methods=["GET"])
def mostrar_cliente():
    cliente = ClienteService.listar_cliente_ativos()
    return cliente, 200


@clientes_bp.route("/<int:id>" methods=["GET"])
def mostrar_clienteId(id):
    cliente

@clientes_bp.route("/", methods=["POST"])
def criar_cliente():
    dados = request.json

    if not dados:
        return {"Erro": "JSON invalido!"},400
    
    schema = ClienteCreateSchema(dados)

    if not schema.valido():
        return {"Erros":schema.erros},400
    
    try:
        cliente = ClienteService.criar_cliente(schema)
        return cliente, 201
    
    except ValueError as e:
        return {"Erro": str(e)},400
    
    except Exception as e:
        return {"Erro": str(e)},500
    
    

    