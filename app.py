import os.path
from flask import Flask
from routes.content import main
from routes.user import user
from extended import db
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = 'alohomora'

    app.config['MYSQL_HOST'] = "0.0.0.0"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = "DBAdmin123*"
    app.config['MYSQL_DB'] = "TODOLIST"
    app.config['MYSQL_PORT'] = 3306
    app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

    app.register_blueprint(main)
    app.register_blueprint(user)
    db.init_app(app)

    return app