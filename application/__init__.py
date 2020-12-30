from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_mail import Mail
import socketio
import socket


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'confirmareemailtrazneascaintinedeprost'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True


mail = Mail(app)
mysql = MySQL(app)

from application import routes