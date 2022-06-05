class Tarefa:
    def __init__(self, titulo, descricao, data, id=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data = data


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
