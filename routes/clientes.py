from flask import Blueprint, jsonify, request
from services import ClienteService
from schema import ClienteCreateSchema

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes" )

@clientes_bp.route("/", methods=["GET"])
def mostrar_cliente():
    cliente = ClienteService.listar_cliente_ativos()
    return cliente, 200

@clientes_bp.route("/todos", methods=["GET"])
def mostrar_cliente_todas():
    cliente = ClienteService.listar_cliente_todos()
    return cliente, 200

@clientes_bp.route("/<int:id>", methods=["GET"])
def mostrar_clienteId(id):
    cliente = ClienteService.listar_cliente_por_id(id)
    if cliente:
        return cliente, 200
    return {"Erro": "Cliente não existe"},404


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
    

@clientes_bp.route("/<int:id>",methods=["PUT"])
def atualizarClientecompleto(id):
    dados = request.json
    if not dados:
        return {"Erro": "Json invalido!"}
    
    schema = ClienteCreateSchema(dados)
    if not schema.eh_valido():
        return {"Erros":schema.erros},400
    
    certo = ClienteService.atualizarClienteCompleto(id, { "nome":schema.nome, "email":schema.email,"senha":schema.senha})
    if certo:
        return {"mensagem": "Atualizado com sucesso"}, 200
    return {"Erro": "Cliente não encontrado"},404
    

    

    # def atualizar_cliente(id, dados):
    # campos = []
    # valores = []

    # if "nome" in dados:
    #     campos.append("nome=%s")
    #     valores.append(dados["nome"])

    # if "email" in dados:
    #     campos.append("email=%s")
    #     valores.append(dados["email"])

    # if "situacao" in dados:
    #     campos.append("situacao=%s")
    #     valores.append(dados["situacao"])

    # if not campos:
    #     return

    # valores.append(id)

    # sql = f"UPDATE Clientes SET {', '.join(campos)} WHERE id=%s"
    # dbcursor.execute(sql, tuple(valores))
    # db.commit()
