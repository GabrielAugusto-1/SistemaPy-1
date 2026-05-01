from database.db import dbcursor, conexao
from models import Cliente

class ClienteService:

    @staticmethod
    def listar_cliente_ativos():
        dbcursor.execute("SELECT id, nome, email,situacao FROM Clientes WHERE situacao = true")
        rows = dbcursor.fetchall()

        return [Cliente.peloDB(row).virarJSON() for row in rows]

    
    @staticmethod
    def listar_cliente_todos():
        dbcursor.execute("SELECT id, nome, email, situacao FROM Cliente" )
        rows = dbcursor.fetchall()

        return [Cliente.peloDB(row).virarJSON() for row in rows]
    

    @staticmethod
    def listar_cliente_por_id(id):
        dbcursor.execute("select id nome, email, situacao from Cliente where id=%s",id )
        linha = dbcursor.fetchone()


    
    @staticmethod
    def criar_cliente(schema):
  
        dbcursor.execute("select id from clientes where email = %s", (schema.email,))
        if dbcursor.fetchone():
            raise ValueError("Email ja esta cadastrado")
     
        senhahash = schema.senha

        dbcursor.execute("""
insert into clientes (nome, email, senha, situacao) values (%s, %s, %s, %s) returning id""", (schema.nome, schema.email, senhahash, True))
        
     
        novoid = dbcursor.fetchone()[0]
        conexao.commit()
        cliente = Cliente(novoid,nome=schema.nome,email=schema.email,senha=None,situacao=True)
        return cliente.virarJSON()


