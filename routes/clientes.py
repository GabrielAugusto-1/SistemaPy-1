from flask import Blueprint, jsonify, request
from services import ClienteService
from schema import ClienteCreateSchema
from database import conexao

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes" )

@clientes_bp.route("/", methods=["GET"])
def mostrar_cliente():
    cliente = ClienteService.listar_cliente_ativos()
    return cliente, 200


@clientes_bp.route("/<int:cliente_id>", methods=["GET"])
def mostrar_clienteId(cliente_id):
    cliente = ClienteService.listar_cliente_por_id(cliente_id)
    if cliente:
        return cliente, 200
    return {"Erro": "Cliente não existe"},404


@clientes_bp.route("/", methods=["POST"])
def criar_cliente():
    dados = request.json

    if not dados:
        return {"Erro": "JSON invalido!"},400
    
    schema = ClienteCreateSchema(dados)

    if not schema.eh_valido():
        return {"Erros":schema.erros},400
    
    try:
        cliente = ClienteService.criar_cliente(schema)
        return cliente, 201
    
    except ValueError as e:
        conexao.rollback()
        return {"Erro": str(e)},400
    
    except Exception as e:
        conexao.rollback()
        return {"Erro": str(e)},500
    

@clientes_bp.route("/<int:cliente_id>",methods=["PUT"])
def atualizarClientecompleto(cliente_id):
    dados = request.json
    if not dados:
        return {"Erro": "Json invalido!"}
    
    schema = ClienteCreateSchema(dados)
    if not schema.eh_valido():
        return {"Erros":schema.erros},400
    try:
        atualizados = ClienteService.atualizarClienteCompleto(cliente_id, { "nome":schema.nome, "email":schema.email,"senha":schema.senha})
    except Exception as e:
        conexao.rollback()
        return {"Erro": str(e)},500
    
    if atualizados == 0:
        return{"Erro": "Usuario não encotrado"},404
    return {"mensagem": f"Atualizado com sucesso: {atualizados}"}, 200

@clientes_bp.route("/<int:cliente_id>", methods=["PATCH"])

@clientes_bp.route("/<int:cliente_id>", methods=["DELETE"])
def inativarCliente(cliente_id):
    try:
        verificar = ClienteService.InativarCliente(cliente_id)
    except Exception as e:
        return {"Erro": str(e)},500

    if verificar == 0:
        return {"Erro": "Cliente não encontrado"},404
    return{"Mensagem": f"Inativado com sucesso {verificar}"},200



@clientes_bp.route("/ativar/<int:cliente_id>", methods=["PATCH"])
def ativarCliente(cliente_id):
    try:
        verificar = ClienteService.ativarCliente(cliente_id)
    except Exception as e:
        return {"Erro": str(e)},500

    if verificar == 0:
        return {"Erro": "Cliente não encontrado"},404
    return{"Mensagem": f"Ativado com sucesso {verificar}"},200
    
@clientes_bp.route("/<int:cliente_id>", methods=["PATCH"])
def atualizarClienteParcial(cliente_id):
    dados = request.json
    if not dados:
        return {"Erro": "JSON invalido!"}



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
