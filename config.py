from flask_mysqldb import MySQL
from flask_mail import Mail
import socket




class Config(object):
   MYSQL_HOST = 'localhost'
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = '783326'
   MYSQL_DB = ''

   MAIL_SERVER = 'mail.zenic.ro'
   MAIL_USERNAME = 'cosmin@zenic.ro'
   MAIL_PASSWORD = 'Armand27Octombrie'
   MAIL_PORT = 587
   MAIL_USE_TLS = True

