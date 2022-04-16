from flask import Blueprint, Flask, render_template, request, redirect, session, flash, url_for

from db import lista_de_usuarios

user = Blueprint('user', __name__)

@user.get('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@user.post('/autenticar')
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
            return redirect(url_for('user.login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('user.login'))

@user.get('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('main.index'))