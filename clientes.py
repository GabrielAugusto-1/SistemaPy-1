from flask import Flask, Blueprint, request, jsonify

#Flask
clientes_bp = Blueprint("clientes", __name__)


#Variaveis
clientes = [
    { 
        "id":1,
        "nome":"gabriel",
        "email": "gabriel@gmail.com",
        "senha": "123",
        "situacao": True
    },
     { 
        "id":2,
        "nome":"klein",
        "email": "klein@gmail.com",
        "senha": "123",
        "situacao": True
    },
     { 
        "id":3,
        "nome":"sung",
        "email": "sung@gmail.com",
        "senha": "123",
        "situacao": False
    },
     { 
        "id":4,
        "nome":"Moretti",
        "email": "Moretti@gmail.com",
        "senha": "123",
        "situacao": True
    }
]
prox_id = 5
camposNec = ["senha", "email", "nome"] 

#sistema


#funções
def formatarCliente(c):
    return{
        "id": c["id"],
        "nome": c["nome"],
        "email":c["email"],
        "situacao": c["situacao"]
        }





@clientes_bp.route("/clientes", methods=["GET"])
def listar_clientesAtivos():
    return [formatarCliente(c) for c in clientes if c["situacao"]]

@clientes_bp.route("/clientes/todos", methods=["GET"])
def mostrar_todos():
    return [formatarCliente(c) for c in clientes]

@clientes_bp.route("/clientes", methods=["POST"])
def cadastrar_cliente():
    global prox_id

    dados = request.json

    if not dados:
       return {"Erro": "Nenhum json foi encotrado! O parametros são: 'nome' 'email' 'senha'"}, 400
    
    faltando = not all(campo in dados for campo in camposNec)

  
    
    if faltando:
        return{"Erro": "Campos necessarios: 'nome' 'email' 'senha'"}, 400
    
    
    cliente = {
        "id": prox_id,
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"],
        "situacao": True
  }
    
    clientes.append(cliente)
    prox_id += 1

    return {"Mensagem": "Usuario validado e cadastrado com sucesso!"}, 201

@clientes_bp.route("/clientes/<int:id>", methods=["GET"])
def mostrar_id(id):
    for dados in clientes:
        if dados["id"] == id:
            return {
                "id": dados["id"],
                "nome": dados["nome"],
                "email": dados["email"],
                "situacao": dados["situacao"]
            }
    
    return {"Erro": "Nenhum cliente foi encontrado!"}, 404

@clientes_bp.route("/clientes/<int:id>", methods=["DELETE"])
def inativar_id(id):
    for dados in clientes:
        if dados["id"] == id:
            dados["situacao"] = False
            return {"mensagem": "Seu cliente foi deixado como inativo com sucesso!", "cliente": dados }
        
    return {"Erro": "Cliente não encontrado"},404



@clientes_bp.route("/clientes/<int:id>", methods=["PUT"])
def editar_cliente(id):
    novosdados = request.json
    if not novosdados:
        return {"Erro": "Mande algum arquivo json valido"},400
    
    if not any(novosdados.get(campo) not in [None, ""] for campo in ["email", "senha", "nome"]):
        return {"Erro": "Voce não esta alterando nada, os campos sao 'nome' ou 'senha' ou 'email'"},400
    
    for dados in clientes:

        if dados["id"] == id:
            dadosantes = dados.copy()
            dados["nome"] = novosdados.get("nome", dados["nome"])
            dados["email"] = novosdados.get("email", dados["email"])
            dados["senha"] = novosdados.get("senha", dados["senha"])

            return {
                "Mensagem": "A alteração foi feita com sucesso!",
                "Dados Antigos": dadosantes,
                "Dados Atualizados": dados
            },200
    
    return {"Erro": "Cliente não encontrado"},404


