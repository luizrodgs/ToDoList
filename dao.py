from models import Tarefa, Usuario

SQL_DELETA_TAREFA = 'delete from tbTarefa where ID = %s'
SQL_TAREFA_POR_ID = 'SELECT ID, TITULO, DESCRICAO, DATA_FINAL from tbTarefa where ID = %s'
SQL_USUARIO_POR_ID = 'SELECT ID, NOME, SENHA from tbUsuario where id = %s'
SQL_ATUALIZA_TAREFA = 'UPDATE tbTarefa SET TITULO=%s, DESCRICAO=%s, DATA_FINAL=%s where ID = %s'
SQL_BUSCA_TAREFA = 'SELECT ID, TITULO, DESCRICAO, DATA_FINAL from tbTarefa'
SQL_CRIA_TAREFA = 'INSERT into tbTarefa (TITULO, DESCRICAO, DATA_FINAL) values (%s, %s, %s)'

class TarefaDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, tarefa):
        cursor = self.__db.connection.cursor()

        if (tarefa.id):
            cursor.execute(SQL_ATUALIZA_TAREFA, (tarefa.titulo, tarefa.descricao, tarefa.data, tarefa.id))
        else:
            cursor.execute(SQL_CRIA_TAREFA, (tarefa.titulo, tarefa.descricao, tarefa.data))
            tarefa.id = cursor.lastrowid
        self.__db.connection.commit()
        return tarefa

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_TAREFA)
        tarefas = traduz_tarefas(cursor.fetchall())
        return tarefas

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_TAREFA_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_TAREFA, (id, ))
        self.__db.connection.commit()

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_tarefas(tarefas):
    def cria_tarefa_com_tupla(tupla):
        return Tarefa(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_tarefa_com_tupla, tarefas))

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
