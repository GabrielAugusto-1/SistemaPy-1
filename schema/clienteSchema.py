from utils import limpar

class ClienteCreateSchema:
   
    def __init__(self, dados):
        self.nome = dados.get("nome")
        self.email = dados.get("email")
        self.senha = dados.get("senha")
       
        self.erros = []

        try:
            self.nome = limpar(self.nome)
            self.email = limpar(self.email)
            self.senha = str(self.senha).strip() if self.senha is not None else None
        except Exception as e:
            self.erros.append(f"Erro ao converter tipos: {str(e)}")


        campos_validos = {"nome", "email", "senha"}
        campos_recebidos = set(dados.keys())

        campos_invalidos = campos_recebidos - campos_validos

        if campos_invalidos:
            self.erros.append(f"Campo invalidos: {list(campos_invalidos)}")
        self.erros.extend(self.validarCliente())
        
    
    def validarCliente(self):
        erros = []

        if not self.nome or not self.nome.strip():
            erros.append("Campo e valores de nome obrigatorio")
            
        if not self.email or not self.email.strip():
            erros.append("Campo e valores de email obrigatorio")

        if self.email:
            if not "@" in self.email:
                erros.append("Email invalido! Verique se há @")
    
        if not self.senha or not self.senha.strip():
            erros.append("Campo e valores de senha obrigatorio")
        


        return erros
    
    def eh_valido(self):
        return len(self.erros) == 0





class ClienteUpdateSchema:
    def __init__(self, dados):
        self.erros = []
        self.dados = {}

        campos_validos = ["nome","email", "senha"]


        for campo, valor in dados.items():
            if campo not in campos_validos:
                self.erros.append({f"Campo invalido {campo}"})

            if campo in ["nome", "email", "senha"]:
                valor = limpar(valor)

            self.dados[campo] = valor
        self.validar()
    
    def validar(self):
        if "email" in self.dados.items():
            if "@" in self.dados["email"]:
                self.erros.append("Erro: Email invalido sem '@'")
    
    def eh_valido(self):
        return self.erros == 0
        

# class ClienteCreateSchema:

#     def __init__(self, dados):
#         self.erros = []

#         self.nome = dados.get("nome")
#         self.email = dados.get("email")
#         self.senha = dados.get("senha")

#         self.validar()

#     def validar(self):

#         if not self.nome:
#             self.erros.append("Nome é obrigatório")

#         if not self.email:
#             self.erros.append("Email é obrigatório")

#         if not self.senha:
#             self.erros.append("Senha é obrigatória")

#     def valido(self):
#         return len(self.erros) == 0







# from utils import limpar

# class ClienteCreateSchema:

#     def __init__(self, dados):
#         self.erros = []

#         self.nome = limpar(dados.get("nome"))
#         self.email = limpar(dados.get("email"))
#         self.senha = limpar(dados.get("senha"))

#         self.validar()

#     def validar(self):

#         if not self.nome:
#             self.erros.append("Nome é obrigatório")

#         if not self.email:
#             self.erros.append("Email é obrigatório")

#         if not self.senha:
#             self.erros.append("Senha é obrigatória")

#     def valido(self):
#         return len(self.erros) == 0






# class ClienteCreateSchema:
#     def __init__(self, dados):
#         self.nome = dados.get("nome")
#         self.email = dados.get("email")
#         self.senha = dados.get("senha")


#         self.validar()
    
#     def validar(self):
#         if not self.nome or not self.nome.strip():
#             return {"Erro", "Campo nome obrigatorio"}







