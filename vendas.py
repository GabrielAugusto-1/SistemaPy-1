from flask import Flask,Blueprint, request,jsonify

vendas_bp = Blueprint("vendas", __name__)

vendas = []
campos_obrigatorios = ["clienteid","produtoid", "quantidade"]

@vendas_bp.route("/vendas", methods=["GET"])
def mostrar_vendas():
    return vendas

@vendas_bp.route("/vendas", methods=["POST"])
def criar_venda():
    dados = request.json
    if not dados:
        return {"Erro", "Envie um JSON valido!"}, 400
    if not all(campo in dados for campo in campos_obrigatorios):
        