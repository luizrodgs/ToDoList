from flask import Blueprint, render_template, request, redirect, session, flash, url_for, send_from_directory, current_app
from dao import TarefaDao, UsuarioDao
from models import Tarefa, Usuario
from extended import db
import os
import time

main = Blueprint('main', __name__)

tarefa_dao = TarefaDao(db)
usuario_dao = UsuarioDao(db)


@main.get('/')
def lista():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.lista')))
    lista_de_tarefas = tarefa_dao.listar()
    return render_template('index.html', titulo='Lista de Tarefas', lista_de_tarefas=lista_de_tarefas)


@main.get('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.novo')))
    return render_template('novo.html', titulo='Adicionar Tarefa')


@main.get('/sobre')
def sobre():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.novo')))
    return render_template('sobre.html', titulo='Sobre o Projeto')


@main.post('/criar')
def criar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    data = request.form['data']
    tarefa = Tarefa(titulo, descricao, data)
    tarefa_dao.salvar(tarefa)

    arquivo = request.files['arquivo']
    upload_path = current_app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{tarefa.id}-{timestamp}.jpg')
    flash('Tarefa adicionada com sucesso!')
    return redirect(url_for('main.lista'))


@main.get('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('user.login', proxima=url_for('main.editar')))
    tarefa = tarefa_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editar Tarefa', tarefa=tarefa, capa_tarefa=nome_imagem or 'capa.jpg')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(current_app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_PATH'], arquivo))
    except:
        pass


@main.post('/salvar')
def salvar():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    data = request.form['data']
    tarefa = Tarefa(titulo, descricao, data, id=request.form['id'])
    arquivo = request.files['arquivo']
    upload_path = current_app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(tarefa.id)
    arquivo.save(f'{upload_path}/capa{tarefa.id}-{timestamp}.jpg')
    tarefa_dao.salvar(tarefa)

    flash('Tarefa salva com sucesso!')
    return redirect(url_for('main.lista'))


@main.get('/delete/<int:id>')
def delete(id):
    tarefa_dao.deletar(id)
    flash('Tarefa apagada com sucesso!')
    return redirect(url_for('main.lista'))


@main.get('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    print(nome_arquivo)
    return send_from_directory('uploads', nome_arquivo)
