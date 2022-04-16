from flask import Flask

from routes.content import main

from routes.user import user

def create_app():
    app = Flask(__name__)
    app.secret_key = 'alohomora'
    app.register_blueprint(main)
    app.register_blueprint(user)
    return app
