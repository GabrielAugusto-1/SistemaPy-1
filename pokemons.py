from flask import Flask,request, jsonify,Blueprint
from db import conexao,dbcursor

campoobrigatorio = ["pokemon1", "pokemon2","pokemon3","pokemon4","pokemon5","pokemon6", "nota"]
times = []
pokemons_bp = Blueprint("pokemons",__name__)
dbcursor.execute("select * from pokeTime order by nota")
ttimes = dbcursor.fetchall()
for time in ttimes:
    times.append(
    {
        "id":time[0],
        "pokemon1": time[1],
        "pokemon2": time[2],
        "pokemon3": time[3],
        "pokemon4": time[4],
        "pokemon5": time[5],
        "pokemon6": time[6],
        "nota":time[7]}
    )
def formatarbancopokemon(time):
        return{
        "id":time[0],
        "pokemon1": time[1],
        "pokemon2": time[2],
        "pokemon3": time[3],
        "pokemon4": time[4],
        "pokemon5": time[5],
        "pokemon6": time[6],
        "nota":time[7]}

@pokemons_bp.route("/pokemons/times")
def mostrar_time():
    return times

@pokemons_bp.route("/pokemons/times", methods=["POST"])
def cadastrartime():
    dados = request.json
    if not dados:
        return {"erro": "Mande um JSON valido"},400
    
    faltando = all(campo in dados for campo in campoobrigatorio)
    if not faltando:
        return {"Erro": "Esta faltando algum dos campos 'pokemon1', 'pokemon2'...'pokemon6'  e 'nota'"},400
    try:
        nota = float(dados["nota"])
    except ValueError:
        return {"Erro": "A nota deve ser um numero"}

    try:
        poke1 = dados["pokemon1"]
        poke2 = dados["pokemon2"]
        poke3 = dados["pokemon3"]
        poke4 = dados["pokemon4"]
        poke5 = dados["pokemon5"]
        poke6 = dados["pokemon6"]

        dbcursor.execute("insert into pokeTime (pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6, nota) values (%s,%s,%s,%s,%s,%s,%s)", (poke1,poke2,poke3,poke4,poke5,poke6,nota))
        conexao.commit()
        return {"Sucesso": "Seu time de pokemon foi cadastrado!"}
    except Exception as e:
        return{"Erro": str(e)},500

@pokemons_bp.route("/pokemons/times/<int:id>", methods=["GET"])
def mostrar_pokemonid(id):
    dbcursor.execute("Select * from poketime where id = %s", (id,))
    pokemonid = dbcursor.fetchone()
    if pokemonid:
        return formatarbancopokemon(pokemonid),200
    return {"Time não encontrado (id)"},404

@pokemons_bp.route("/pokemons/times/<int:id>", methods=["PUT"])
def alterartimeid(id):
    dados = request.json
    if not dados:
        return {"erro": "Mande um JSON valido"},400
    
    faltando = all(campo in dados for campo in campoobrigatorio)
    if not faltando:
        return {"Erro": "Esta faltando algum dos campos 'pokemon1', 'pokemon2'...'pokemon6'  e 'nota'"},400
    try:
        nota = float(dados["nota"])
    except ValueError:
        return {"Erro": "A nota deve ser um numero"},400

    try:
        poke1 = dados["pokemon1"]
        poke2 = dados["pokemon2"]
        poke3 = dados["pokemon3"]
        poke4 = dados["pokemon4"]
        poke5 = dados["pokemon5"]
        poke6 = dados["pokemon6"]

        dbcursor.execute("update pokeTime set pokemon1=%s, pokemon2=%s, pokemon3=%s, pokemon4=%s, pokemon5=%s, pokemon6=%s, nota=%s where id = %s returning id ", (poke1,poke2,poke3,poke4,poke5,poke6,nota,id))
        idretornado = dbcursor.fetchone()

        if not idretornado:
            return {"Erro":"Time não encontrado (id)"},404
        conexao.commit()
        return {"Sucesso": "Seu time de pokemon foi alterado!"}
    except Exception as e:
        return{"Erro": str(e)},500    