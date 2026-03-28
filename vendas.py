from flask import Blueprint, request,jsonify
from clientes import clientes
from produtos import produtos

vendas_bp = Blueprint("vendas", __name__)


prox_id = 3
vendas = [
    {
        "id":1,
        "idproduto":1,
        "idcliente":2,
        "quantidade":4,
        "situacao": True,
        "valor_total": 1519.96
    },
    {
        "id":2,
        "idproduto":1,
        "idcliente":2,
        "quantidade":4,
        "situacao": False,
        "valor_total": 1519.96
    }
]
campos_obrigatorios = ["idcliente","idproduto", "quantidade"]

def atualizarvenda(venda, quantidade, quantiadeantiga):
    produto = next((produto for produto in produtos if produto["id"] == venda["idproduto"]), None)

    if not produto:
        return {"Erro": "Produto não existe"}, 404
    
    if produto["situacao"]:
        return{"Erro": "produto inativo"}, 400

    if quantiadeantiga: #5
        if quantiadeantiga < quantidade: #10
            validar = quantidade - quantiadeantiga
            if not validar > produto["estoque"]:
                return
            produto["estoque"] = produto["estoque"] - validar
            venda["valor_total"] = produto["preco"] * quantidade
            atualizarEstoque = produto["estoque"] - validar
            
            return atualizarEstoque

        elif quantidade < quantiadeantiga:
            validar = quantiadeantiga - quantidade
            if not validar >produto["estoque"]:
                return
            
            atualizarEstoque = produto["estoque"] + validar
            return atualizarEstoque


@vendas_bp.route("/vendas", methods=["GET"])
def mostrar_vendas():
    return [validas for validas in vendas if validas["situacao"]],200

@vendas_bp.route("/vendas/todos", methods=["GET"])
def mostrar_todas_vendas():
    return vendas,200

@vendas_bp.route("/vendas", methods=["POST"])
def criar_venda():
    global prox_id
    dados = request.json

    #validações
    if not dados:
        return {"Erro": "Envie um JSON valido!"}, 400
    
    if not all(campo in dados for campo in campos_obrigatorios):
        return {"erro":"Campos Obrigatorios: 'idcliente' 'idproduto' 'quantidade'"},400
    

    try:
        idcliente = int(dados["idcliente"])
        idproduto = int(dados["idproduto"])
        quantidade = int(dados["quantidade"])
        if quantidade <= 0:
            return {"Erro": "A quantidade deve ser um valor positivo"},400
        if idproduto <= 0:
            return {"Erro": "O idproduto deve ser um ID, ou seja um numero inteiro"},400
        if idcliente <= 0:
            return {"Erro": "O idcliente deve ser um ID, ou seja um numero inteiro"},400
    except ValueError:
        return{"Erro":"Os valores deve ser um numero inteiro"},400

    
    cliente =  next((cliente for cliente in clientes if cliente["id"] == idcliente), None)
    
    if not cliente:
        return {"Erro": "O id do cliente não pertence a ninguem! O cliente não existe!"},400
    
    if not cliente["situacao"]:
        return {"Erro": "Este cliente esta inativo ou foi deletado"}, 400
   
    produto = next((produto for produto in produtos if produto["id"] == idproduto),None)

    if not produto:
         return {"Erro": "O id do produto não pertence a ninguem! O produto não existe!"},404
    
    if not produto["situacao"]:
        return {"Erro": "Este produto esta inativo ou foi deletado"},400


    if produto["estoque"] < quantidade:
        return {"Erro": "Não ha estoque suficiente", "estoque do produto": produto["estoque"]},400
    
    valor_total = produto["preco"] * quantidade
    #tirar do estoque
    produto["estoque"] -= quantidade
    
    #criar venda
    venda = {
        "id": prox_id,
        "idcliente":idcliente,
        "idproduto":idproduto,
        "quantidade":quantidade,
        "valor_total": valor_total,
        "situacao": dados.get("situacao", True)
    }
    prox_id += 1
    vendas.append(venda)
    return {"mensagem": "Sua venda foi criada com sucesso", "venda": venda, "estoque restante": produto["estoque"], "cliente": cliente, "produto": produto},201

@vendas_bp.route("/vendas/<int:id>", methods=["GET"])
def mostrar_vendas_id(id):
    for venda in vendas:
        if venda["id"] == id:
            return venda,200
        
    return {"Erro": "Venda não existe"}, 404

@vendas_bp.route("/vendas/<int:id>", methods=["DELETE"])
def deletar_venda_id(id):
    for venda in vendas:
        if venda["id"] == id:
            produto = next((produto for produto in produtos if produto["id"] == venda["idproduto"]), None)
            
            if not produto:
                return {"Erro": "O produto não existe mais"},404
            
            if not produto["situacao"]:
                return {"Erro": "O produto se tornou inativo"}, 400
            
            produtoantes = produto.copy()

            produto["estoque"] += venda["quantidade"]
            venda["situacao"] = False

            return{"Estoque antes": produtoantes["estoque"], "Estoque atualizado": produto["estoque"], "venda": venda},200

@vendas_bp.route("/vendas/<int:id>", methods=["PUT"])
def editar_venda(id):
    for venda in vendas:
        if venda["id"] == id:
            vendaantes = venda.copy()
            dados = request.json
            if not dados:
                return {"Erro": "Envie um JSON valido!"},400
            
            if not any(campo in dados for campo in campos_obrigatorios):
                return {"Erro": "Precisa ter algum campo no Json (campos: 'idcliente' 'idproduto' 'quantidade')"}, 400
            
            if "idproduto" in dados:
                try:
                    idproduto = int(dados["idproduto"])
                except ValueError:
                    return {"Erro": "Quantidade não é um numero inteiro"},400
                
                if idproduto <= 0:
                    return {"Erro": "idproduto tem que ser um numero positivo"},400
             
                novoproduto = next((produto for produto in produtos if produto == idproduto),None)
                if not novoproduto:
                    return {"Erro": "id de produto não encontrado"},404
                if not novoproduto["situacao"]:
                    return{"Erro": "Produto inativo"}
                
                if not venda["idproduto"] == novoproduto["id"]:
                    venda["quantidade"] == 0

                venda["idproduto"] = novoproduto["id"]
                return{"sucesso": "ateh aqui por enquanto"}
              
                
                
                

            if "quantidade" in dados:
                try:
                    quantidade = int(dados["quantidade"])
                except ValueError:
                    return {"Erro": "Quantidade não é um numero inteiro"},400
                
                if quantidade <= 0:
                    return {"Erro": "Quantidade tem que ser um numero positivo"},400
                
                atualizarEstoque = atualizarvenda(venda, quantidade, vendaantes)
                novoproduto["estoque"] = atualizarEstoque               
                
            if "idcliente" in dados:
                try:
                    idcliente = int(dados["idcliente"])
                except ValueError:
                    return {"Erro": "O valor do idcliente deve ser um numero inteiro"},400
                if idcliente <= 0:
                    return {"Erro": "idcliente tem que ser um numero positivo"},400

                novocliente = next((cliente for cliente in clientes if cliente["id"] == idcliente), None)

                if not novocliente:
                    return {"Erro": "Cliente não existe"}, 404
                
                if not novocliente["situacao"]:
                    return{"Erro": "Cliente foi deixado como inativo"}, 400
                
            atualizacao = {}
            if idcliente:
                atualizacao.update({"idcliente": idcliente})
            if idproduto:
                atualizacao.update({"idproduto":idproduto})
            if quantidade:
                atualizacao.update({"quantidade":quantidade})
        
            venda = {
                **venda,**atualizacao
            }
            
            return{"venda antes": vendaantes, "venda editada":venda,"produto Antes atualizado:":produtos[vendaantes["idproduto"] - 1]}
                


            