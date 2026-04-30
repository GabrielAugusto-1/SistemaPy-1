from database import dbcursor, conexao

class Cliente:
    def __init__(self, id,nome, email, senha, situacao=True):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.situacao = situacao

    def virarJSON(self):
        return{
            "id": self.id, "nome": self.nome, "email":self.email, "senha": None, "situacao": self.situacao
        }
    
    @staticmethod
    def peloDB(row):
        return Cliente(
            id=row[0],
            nome=row[1],
            email=row[2],
            senha=None,
            situacao=row[3])
                            
        