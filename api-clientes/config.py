from flask.helpers import get_env
from app import app
from flaskext.mysql import MySQL
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# flaskext.mysql é uma extenção para conectar o flask com o MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASS')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST') # preencher com o db_host
mysql.init_app(app)
