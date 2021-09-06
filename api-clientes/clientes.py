import pymysql
from app import app, metrics
from config import mysql
from flask import jsonify
from flask import flash, request,Response
from auth import BasicAuth
from flask import Flask, render_template, json, request,redirect,session
from flaskext.mysql import MySQL
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import start_http_server, Summary
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


#static info as metric
metrics.info("app_info", "Metricas API Clientes", version="1.0.0")

#Adiciona um cliente  --- OK
@app.route("/api/clientes", methods=["POST"])
def adiciona_cliente():
	try:
		_json=request.json
		_nome=_json['nome']
		_cpf=_json['cpf']
		_email=_json['email']
		_telefone=_json['telefone']
		conn=mysql.connect()
		cursor = conn.cursor()
		if _nome and _cpf and _email and _telefone and request.method=="POST":
			sqlQuery="INSERT INTO cadastro.clientes (nome, cpf, email, telefone) VALUES (%s,%s, %s, %s);"
			bindData=(_nome, _cpf, _email, _telefone)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Cliente cadastrado com sucesso!')
			response.status_code=200
			return response
		else:
			return not_found()	
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close()
		conn.close()

#Altera informações no cadastro de um cliente específico --- OK
@app.route('/api/clientes/<int:id_cliente>', methods=['PUT'])
def atualiza_cliente(id_cliente):
	try:
		conn = mysql.connect()
		cursor=conn.cursor()
		_json = request.json
		_nome = _json['nome']
		_cpf = _json['cpf']
		_email = _json['email']
		_telefone = _json['telefone']
		_id_cliente = _json['id_cliente']
		if _nome and _cpf and _email and _telefone and _id_cliente and request.method == 'PUT':
			sqlQuery = "UPDATE cadastro.clientes SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE id_cliente=%s"
			bindData = (_nome, _cpf, _email, _telefone, _id_cliente,)
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('Cliente atualizado com sucesso!')
			response.status_code = 200
			return response
		else:
			return not_found()	
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()
   
#Deleta informações de um clientes específico --- OK
@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def deleta_cliente(id_cliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cadastro.clientes WHERE id_cliente =%s", (id_cliente))
		conn.commit()
		response = jsonify('Cliente deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

#Retorna todas as informações de todos os clientes --- OK
@app.route('/api/clientes', methods=["GET"])
def retorna_cliente():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM cadastro.clientes;")
		showRows = cursor.fetchall()
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}),500
	finally:
		cursor.close() 
		conn.close()

#Retorna informações de um clientes específico --- OK
@app.route('/api/clientes/<int:id_cliente>', methods=["GET"])
def retorna_cliente_id(id_cliente):

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id_cliente, nome, cpf, email, telefone FROM cadastro.clientes WHERE id_cliente =%s", id_cliente)
		view_Rows = cursor.fetchall()
		if not view_Rows:
			return Response("Cliente não encontrado."), 404
		response = jsonify(view_Rows)
		response.status_code = 200
		return response     
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()
  
@app.route("/healthcheck/clientes")
def hello():
    return "Ok."

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()})

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)