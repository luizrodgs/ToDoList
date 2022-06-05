from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from dao import TarefaDao, UsuarioDao
from extended import db

user = Blueprint("user", __name__)

tarefa_dao = TarefaDao(db)
usuario_dao = UsuarioDao(db)


@user.get("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@user.post("/autenticar")
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form["usuario"])
    if usuario:
        if usuario.senha == request.form["senha"]:
            session["usuario_logado"] = usuario.id
            flash(usuario.nome + " logou com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
    else:
        flash("Usuário não logado.")
        return redirect(url_for("user.login"))


@user.get("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Usuário deslogado com sucesso!")
    return redirect(url_for("main.lista"))
