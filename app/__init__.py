from flask import Flask
from flask_login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
# import server
# host = server.Server()  # server

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webappdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.setup_app(app)

import models
import server
host = server.Server()
import views
