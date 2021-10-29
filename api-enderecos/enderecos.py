import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request,Response
from flask import request, render_template


#Adiciona um endereço para um cliente específico 
@app.route("/api/enderecos/add", methods=["POST"])
def adiciona_endereco():
	try:
		_json=request.json
		_id_cliente=_json['id_cliente']
		_CEP=_json['CEP']
		_Endereco=_json['Endereco']
		_Numero=_json['Numero']
		_Complemento=_json['Complemento']
		_Bairro=_json['Bairro']
		_Localidade=_json['Localidade']
		_UF=_json['UF']
		conn=mysql.connect()
		cursor=conn.cursor()
		if _id_cliente and _CEP and _Endereco and _Numero and _Complemento and _Bairro and _Localidade and _UF and request.method=="POST":
			sqlQuery="INSERT INTO cadastro.enderecos (id_cliente,CEP,Endereco,Numero,Complemento,Bairro,Localidade,UF) VALUES (%s,%s,%s,%s,%s, %s, %s, %s);"
			bindData=(_id_cliente,_CEP, _Endereco,_Numero, _Complemento, _Bairro,_Localidade,_UF)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Endereço atribuído com sucesso!')
			response.status_code=200
			return response
		else:
			return not_found()	
	except Exception as error:
		return jsonify({"error":f"{error}"}),500
	finally:
		cursor.close() 
		conn.close()

#Altera infromações de um endereço específico
@app.route("/api/enderecos/change/<int:id_end>", methods=["PUT"])
def atualiza_endereco(id_end):
	try:
		conn = mysql.connect()
		cursor=conn.cursor()
		_json=request.json
		_id_cliente =_json['id_cliente']
		_id_end=_json['id_end']
		_CEP=_json['CEP']
		_Endereco=_json['Endereco']
		_Numero=_json['Numero']
		_Complemento=_json['Complemento']
		_Bairro=_json['Bairro']
		_Localidade=_json['Localidade']
		_UF=_json['UF']
		if _id_cliente and _CEP and _Endereco and _Numero and _Complemento and _Bairro and _Localidade and _UF and _id_end and request.method =="PUT":
			sqlQuery="UPDATE cadastro.enderecos SET id_cliente=%s ,CEP=%s ,Endereco=%s,Numero=%s ,Complemento= %s ,Bairro= %s ,Localidade= %s ,UF= %s  WHERE id_end = %s"
			bindData=(_id_cliente,_CEP, _Endereco,_Numero, _Complemento, _Bairro,_Localidade,_UF,_id_end,)
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Alterado com sucesso com sucesso!')
			response.status_code=200
			return response
		else:
			return not_found()	
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()            

#Apaga um endereço específico
@app.route('/api/enderecos/del/<int:id_end>', methods=['DELETE'])
def deleta_endereco(id_end):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("DELETE FROM cadastro.enderecos WHERE id_end =%s", (id_end))
		conn.commit()
		response = jsonify('Endereço deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

#Retorna todos os endereços cadastrados
@app.route('/api/enderecos')
def retorna_endereco():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM cadastro.enderecos")
		showRows = cursor.fetchall()
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

#Retorna um endereço específico
@app.route('/api/enderecos/<int:id_end>', methods=["GET"]) 
def retorna_endereco_id(id_end):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT  id_cliente,id_end,CEP,Endereco,Numero,Complemento,Bairro,Localidade,UF FROM cadastro.enderecos WHERE id_end = %s",  id_end )
		view_Rows = cursor.fetchall()
		if not view_Rows:
			return Response("Endereço não encontrado."),404
		response = jsonify({'result':view_Rows,'status':200,})	
		return response		
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

#Retorna os endereços cadastrados para um cliente específico
@app.route('/api/enderecos/clientes/<int:id_cliente>', methods=["GET"])  
def retorna_endereco_cliente(id_cliente):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT enderecos.CEP,enderecos.Endereco,enderecos.Numero,enderecos.Complemento,enderecos.Bairro,enderecos.Localidade,enderecos.UF,enderecos.id_cliente,clientes.Nome FROM cadastro.enderecos inner  join  cadastro.clientes on clientes.id_cliente = enderecos.id_cliente WHERE enderecos.id_cliente = %s ",id_cliente)
		showRows = cursor.fetchall()
		if not showRows:
			return Response("Registro não encontrado."),404
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

@app.route("/api/enderecos/healthcheck")
def hello():
    return "Ok."

@app.route('/api/enderecos/swagger')
def get_docs():
    print('Preparando Swagger ...')
    return render_template('swaggerui.html')

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5100)
