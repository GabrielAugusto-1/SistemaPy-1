from flask import Flask, Blueprint, request, jsonify
from db import dbcursor,conexao

#Flask
clientes_bp = Blueprint("clientes", __name__)
def CriarClientes():
    dbcursor.execute("select * from clientes")
    return dbcursor.fetchall()

#Variaveis
clientes =[]
cliente = CriarClientes()

for cliente in cliente:
    clientes.append({
        "id": cliente[0],
        "nome": cliente[1],
        "email": cliente[2],
        "senha": cliente[3],
        "situacao": cliente[4]})


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
def formatarClienteBancoSemSenha(c):
    return{
        "id": c[0],
        "nome": c[1],
        "email":c[2],
        "situacao": c[3]
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
    
    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    dbcursor.execute(""" insert into clientes (nome, email, senha, situacao)values (%s, %s,%s,%s) returning id""", (nome, email, senha, True))
    novo_id = dbcursor.fetchone()[0]
    conexao.commit()
    
#     cliente = {
#         "id": prox_id,
#         "nome": dados["nome"],
#         "email": dados["email"],
#         "senha": dados["senha"],
#         "situacao": True
#   }
    
#     clientes.append(cliente)
#     prox_id += 1

    return {"Mensagem": "Usuario validado e cadastrado com sucesso!", "Cliente": {"id": novo_id,"nome":nome,"email":email,"situacao":True}}, 201

@clientes_bp.route("/clientes/<int:id>", methods=["GET"])
def mostrar_id(id):
    
    dbcursor.execute("""select id,nome,email,situacao from clientes where id = %s""", (id,))
    cliente = dbcursor.fetchone()

    if cliente:
        return formatarClienteBancoSemSenha(cliente),200
    


    # if dados["id"] == id:
    #     return {
    #         "id": dados["id"],
    #         "nome": dados["nome"],
    #         "email": dados["email"],
    #         "situacao": dados["situacao"]
    #     }
    
    return {"Erro": "Nenhum cliente foi encontrado!"}, 404

@clientes_bp.route("/clientes/<int:id>", methods=["DELETE"])
def inativar_id(id):
    try:
        dbcursor.execute("update clientes set situacao=%s where id = %s returning id", (False, id))
        idveio = dbcursor.fetchone()
        

        if not idveio:
            return {"Erro": "Cliente não encontrado"},404
        
        conexao.commit()    
        return{"Sucesso":"cliente inativado!"},200
    
    except Exception as e:
        conexao.rollback()
        return{"erro": str(e)},500

    # for dados in clientes:
    #     if dados["id"] == id:
    #         dados["situacao"] = False
    #         return {"mensagem": "Seu cliente foi deixado como inativo com sucesso!", "cliente": dados }
        
    # return {"Erro": "Cliente não encontrado"},404



@clientes_bp.route("/clientes/<int:id>", methods=["PUT"])
def editar_cliente(id):
    novosdados = request.json
    if not novosdados:
        return {"Erro": "Mande algum arquivo json valido"},400
    
    faltando = not all(campo in novosdados for campo in camposNec)

    if faltando:
        return{"Erro": "Campos necessarios: 'nome' 'email' 'senha'"}, 400
    
    nome  = novosdados["nome"]
    email = novosdados["email"]
    senha = novosdados["senha"]
    try:
        dbcursor.execute("update clientes set nome = %s, email=%s, senha=%s where id = %s returning id", (nome,email,senha,id))
        idveio = dbcursor.fetchone()

        if not idveio:
            return {"erro":"cliente não encontrado"},404
        
        conexao.commit()
        return {"Sucesso": "Alteração concluida!"}
    except Exception as e:
        conexao.rollback()
        return {"erro": str(e)}, 500

    # # if not any(novosdados.get(campo) not in [None, ""] for campo in ["email", "senha", "nome"]):
    # #     return {"Erro": "Voce não esta alterando nada, os campos sao 'nome' ou 'senha' ou 'email'"},400
    
    # # for dados in clientes:

    # #     if dados["id"] == id:
    # #         dadosantes = dados.copy()
    # #         dados["nome"] = novosdados.get("nome", dados["nome"])
    # #         dados["email"] = novosdados.get("email", dados["email"])
    # #         dados["senha"] = novosdados.get("senha", dados["senha"])

    # #         return {
    # #             "Mensagem": "A alteração foi feita com sucesso!",
    # #             "Dados Antigos": dadosantes,
    # #             "Dados Atualizados": dados
    # #         },200
    
    # return {"Erro": "Cliente não encontrado"},404


