from flask import request, jsonify, Blueprint
from db import dbcursor, conexao
#Flask
produtos_bp = Blueprint("produtos", __name__)


#funcoes
def criarProdutos():
    dbcursor.execute("Select * from produtos")
    return dbcursor.fetchall()

#Variaveis
produtos = []


# Açoes
produto = criarProdutos()
for p in produto:
    produtos.append({
        "id":p[0],
        "nome":p[1],
        "preco":p[2],
        "estoque":p[3],
        "situacao":p[4]})

def mostrarativos(produtos):
    return [produto for produto in produtos if produto["situacao"]]

id_prox = 5
campos_obrigatorios =["nome", "preco","estoque"]

@produtos_bp.route("/produtos", methods=["GET"])
def mostrar_produtos():
    return [produto for produto in produtos if produto["situacao"]]

@produtos_bp.route("/produtos/todos", methods=["GET"])
def mostrar_todos_produtos():
    return produtos

@produtos_bp.route("/produtos", methods=["POST"])
def criar_produto():
    global id_prox 
    dados = request.json

    #Validações
    if not dados:
        return {"Erro": "Envie um JSON válido"}, 400
    
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"Erro": "Campos obrigatorios: 'nome' 'preco' 'estoque'"},400
    try:
        estoque = int(dados["estoque"])
        preco = float(dados["preco"])
    except:
        return {"Erro": "O preco ou estoque precisam ser numeros", "formatacao": "estoque deve ser inteiro e preco deve ser numérico"},400

    if estoque < 0:
        return {"Erro": "O estoque deve ser um numero positivo"}, 400
    if preco < 0:
        return {"Erro": "O preco deve ser um numero positivo"}, 400
    
    nome = dados["nome"]
    
    dbcursor.execute("insert into produtos (nome,preco,estoque,situacao) values (%s,%s,%s,%s)", (nome,preco,estoque,True))
    
    #colocando produto
    # produto ={
    #     "id": id_prox,
    #     "nome": dados["nome"],
    #     "preco": preco,
    #     "estoque": preco,
    #     "situacao": dados.get("situacao", True)
    # }
    # produtos.append(produto)
    # id_prox += 1
    conexao.commit()
    return {"Mensagem": "Criado com sucesso",
            "produto":produto}, 201

@produtos_bp.route("/produtos/<int:id>", methods=["PUT"])
def editar_produtoid(id):
    for produto in produtos:
        if produto["id"] == id:
            dados = request.json
            if not dados:
                return {"Erro": "Envie um JSON válido"},400
            
            produto_antes = produto.copy()

            # nome (simples)
            if "nome" in dados:
                produto["nome"] = dados["nome"]

            # preco (tem que converter)
            if "preco" in dados:
                try:
                    preco = float(dados["preco"])
                    if preco < 0:
                        return {"Erro": "Preço não pode ser negativo"}, 400
                    produto["preco"] = preco
                except:
                    return {"Erro": "Preço inválido"}, 400

            # estoque (tem que converter)
            if "estoque" in dados:
                try:
                    estoque = int(dados["estoque"])
                    if estoque < 0:
                        return {"Erro": "Estoque não pode ser negativo"}, 400
                    produto["estoque"] = estoque
                except:
                    return {"Erro": "Estoque inválido"}, 400

            return {
                "Mensagem": "Produto atualizado com sucesso",
                "Antes": produto_antes,
                "Depois": produto
            }, 200

    return {"Erro": "Produto não encontrado"}, 404
            
            