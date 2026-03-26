from flask import request, jsonify, Blueprint

#Flask
produtos_bp = Blueprint("produtos", __name__)

#Variaveis
produtos = [
    {
    "id":1,
    "nome": "SSD Nvme 2.0",
    "preco": 379.99,
    "estoque": 7,
    "situacao": True
},
 {
    "id":2,
    "nome": "Caderno Antigonus",
    "preco": 124999.99,
    "estoque": 1,
    "situacao": True
},

 {
    "id":3,
    "nome": "Tridente de kavas",
    "preco": 0,
    "estoque": 0,
    "situacao": False
},
 {
    "id":4,
    "nome": "Fome rastejante",
    "preco": 25000.00,
    "estoque": 7,
    "situacao": True
}]

id_prox = 5
campos_obrigatorios =["nome", "preco" "estoque"]

@produtos_bp.route("/produtos", methods=["GET"])
def mostrar_produtos():
    return [produtos for produtos in produtos if produtos["situacao"]]

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
    

    #colocando produto
    produto ={
        "id": id_prox,
        "nome": dados["nome"],
        "preco": preco,
        "estoque": preco,
        "situacao": dados.get("situacao", True)
    }

    produtos.append(produto)
    id_prox += 1
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
            
            