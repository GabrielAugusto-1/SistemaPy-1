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
        dbcursor.execute("SELECT id, nome, email, situacao FROM Clientes" )
        rows = dbcursor.fetchall()

        return [Cliente.peloDB(row).virarJSON() for row in rows]
    

    @staticmethod
    def listar_cliente_por_id(id):
        dbcursor.execute("select id, nome, email, situacao from Clientes where id=%s",(id,) )
        linha = dbcursor.fetchone()
        if linha:
            return Cliente.peloDB(linha).virarJSON()
        return None


    
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


    @staticmethod
    def atualizarClienteCompleto(cliente_id, dados):
        dbcursor.execute("update clientes set nome=%s, email=%s, senha=%s where id =%s", (dados["nome"],dados["email"],dados["senha"], cliente_id))
        conexao.commit()

        return dbcursor.rowcount
    
    @staticmethod
    def InativarCliente(cliente_id):
        dbcursor.execute("update clientes set situacao=%s where id=%s", (False,cliente_id,) )
        conexao.commit()

        return dbcursor.rowcount

    @staticmethod
    def ativarCliente(cliente_id):
        dbcursor.execute("update clientes set situacao=%s where id=%s", (True,cliente_id,) )
        conexao.commit()

        return dbcursor.rowcount
    
    @staticmethod
    def atualizarClienteParcial(cliente_id, dados):

        campos = []
        valores = []

        for campo, valor in dados.items():
            campos.append(f"{campo}=%s")
            valores.append(valor)

        valores.append(cliente_id)

        sql = f"""
            UPDATE clientes
            SET {", ".join(campos)}
            WHERE id=%s
        """

        dbcursor.execute(sql, tuple(valores))
        conexao.commit()

        return dbcursor.rowcount