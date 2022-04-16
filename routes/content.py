from flask import Blueprint, Flask, render_template, request, redirect, session, flash, url_for
from db import Tarefa, lista_de_tarefas

main = Blueprint('main', __name__)

@main.get('/')
def index():
    return render_template('index.html', titulo='TDL - ToDoList')

@main.get('/lista')
def lista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.lista')))
    return render_template('lista.html', titulo='Lista de Tarefas', lista_de_tarefas=lista_de_tarefas)

@main.get('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.novo')))
    return render_template('novo.html', titulo='Adicionar Nova Tarefa')

@main.post('/criar')
def criar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    data = request.form['data']
    nova_tarefa = Tarefa(titulo, descricao, data)
    lista_de_tarefas.append(nova_tarefa)
    flash('Tarefa adicionada com sucesso!')
    return redirect(url_for('main.lista'))

@main.get('/editar')
def editar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.editar')))
    return render_template('editar.html', titulo='Editar Tarefa')

@main.post('/edit')
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
    return redirect(url_for('main.lista'))

@main.get('/apagar')
def apagar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.apagar')))
    return render_template('apagar.html', titulo='Apagar Tarefa')

@main.post('/delete')
def delete():
    tarefa_a_deletar = request.form['titulodelete']
    for tarefa in lista_de_tarefas:
        if tarefa.titulo == tarefa_a_deletar:
            lista_de_tarefas.remove(tarefa)
            del tarefa
    flash('Tarefa apagada com sucesso!')
    return redirect(url_for('main.lista'))