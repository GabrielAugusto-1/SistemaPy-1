from utils import limpar

class ClienteCreateSchema:

    def __init__(self, dados):
        self.erros = []

        self.nome = limpar(dados.get("nome"))
        self.email = limpar(dados.get("email"))
        self.senha = limpar(dados.get("senha"))

        self.validar()

    def validar(self):

        if not self.nome:
            self.erros.append("Nome é obrigatório")

        if not self.email:
            self.erros.append("Email é obrigatório")

        if not self.senha:
            self.erros.append("Senha é obrigatória")

    def valido(self):
        return len(self.erros) == 0






# class ClienteCreateSchema:
#     def __init__(self, dados):
#         self.nome = dados.get("nome")
#         self.email = dados.get("email")
#         self.senha = dados.get("senha")


#         self.validar()
    
#     def validar(self):
#         if not self.nome or not self.nome.strip():
#             return {"Erro", "Campo nome obrigatorio"}







