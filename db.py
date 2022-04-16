class Tarefa:
    def __init__(self, titulo, descricao, data):
        self.titulo = titulo
        self.descricao = descricao
        self.data = data

        def __str__(self):
            return f'Titulo: {self.titulo} - Descricao: {self.descricao} - Data: {self.data}'

Tarefa1 = Tarefa('Estudar', 'Estudar Programação em Python e Java (OO)', '16/04/2022')
Tarefa2 = Tarefa('Projetar', 'Desenvolver novos projetos de CRUD', '25/04/2022')
Tarefa3 = Tarefa('Academia', 'Ir à academia 5 vezes por semana', '15/04/2022')
Tarefa4 = Tarefa('Banco de Dados','Estudar MySQL','01/05/2022')
Tarefa5 = Tarefa('Soft Skills','Fazer ao menos 3 cursos de SoftSkills na Alura','18/04/2022')
lista_de_tarefas = [Tarefa1, Tarefa2, Tarefa3, Tarefa4, Tarefa5]

class Usuario:
    def __init__(self, nickname, senha):
        self.nickname = nickname
        self.senha = senha
        self.tarefas = []

usuario1 = Usuario('luizrodgs', 'alohomora')
usuario2 = Usuario('user', 'todolist123')

lista_de_usuarios= { usuario1.nickname : usuario1,
                     usuario2.nickname : usuario2,
                     }