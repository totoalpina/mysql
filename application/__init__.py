from flask import Flask
from config import Config
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b"\x8a{\x9e\x02\xbfo\\\xc0\x1a\xff'\x86\xe5\x8e\xf4\xbf"

mysql = MySQL(app)

from application import routes