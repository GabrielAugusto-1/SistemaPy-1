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

    