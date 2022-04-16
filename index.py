from flask import Flask, render_template, request, redirect, session, flash, url_for

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

app = Flask(__name__)
app.secret_key = 'alohomora1'

@app.route('/')
def index():
    return render_template('index.html', titulo='TDL - ToDoList')

@app.route('/lista')
def lista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('lista')))
    return render_template('lista.html', titulo='Lista de Tarefas', lista_de_tarefas=lista_de_tarefas)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Adicionar Nova Tarefa')

@app.route('/criar', methods=['POST',])
def criar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    data = request.form['data']
    nova_tarefa = Tarefa(titulo, descricao, data)
    lista_de_tarefas.append(nova_tarefa)
    flash('Tarefa adicionada com sucesso!')
    return redirect(url_for('lista'))

@app.route('/editar')
def editar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    return render_template('editar.html', titulo='Editar Tarefa')

@app.route('/edit', methods=['POST',])
def edit():
    titulo_a_editar = request.form['tituloedit']
    novo_titulo = request.form['novotitulo']
    nova_descricao = request.form['novadescricao']
    nova_data = request.form['novadata']
    for tarefa in lista_de_tarefas:
        if tarefa.titulo == titulo_a_editar:
            tarefa.titulo = novo_titulo
            tarefa.descricao = nova_descricao
            tarefa.data = nova_data
    flash('Tarefa editada com sucesso!')
    return redirect(url_for('lista'))

@app.route('/apagar')
def apagar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('apagar')))
    return render_template('apagar.html', titulo='Apagar Tarefa')

@app.route('/delete', methods=['POST',])
def delete():
    tarefa_a_deletar = request.form['titulodelete']
    for tarefa in lista_de_tarefas:
        if tarefa.titulo == tarefa_a_deletar:
            lista_de_tarefas.remove(tarefa)
            del tarefa
    flash('Tarefa apagada com sucesso!')
    return redirect(url_for('lista'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in lista_de_usuarios:
        usuario = lista_de_usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)