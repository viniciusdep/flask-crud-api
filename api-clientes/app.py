from flask import Flask
from flask_cors import CORS
from opentelemetry.instrumentation.flask import FlaskInstrumentor



#CORS é um descorador de rotas, podemos passar parametros de metodos ou atenticação
#Exemplo: flask_cors. cross_origin ( origins = "/", methods = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT']


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
CORS(app)
