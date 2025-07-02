#Crie a classe Contato, que representa um contato pra cada linha do db
class Contato:
    def __init__(self, nome, telefone, email=None, id=None): #id inicia nulo, pois vem do db
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        
