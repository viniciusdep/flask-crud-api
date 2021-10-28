import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import request,Response
from flask import render_template, request
from flaskext.mysql import MySQL


#adiciona um produto
@app.route("/api/produtos/add", methods=["POST"])
def adiciona_produto():
    try:
        _json = request.get_json(force = True)
        _json=request.json
        _nome_produto=_json['nome_produto']
        _preco_produto=_json['preco_produto']
        _desc_produto=_json['desc_produto']
        _status=_json['status']
        
        if _nome_produto and _preco_produto and _desc_produto and _status and request.method=="POST":
            sqlQuery="INSERT INTO produtos.catalogo_produtos (nome_produto, preco_produto, desc_produto, status) VALUES (%s, %s, %s, %s);"
            bindData=(_nome_produto, _preco_produto, _desc_produto, _status)
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Produto cadastrado com sucesso!')
            response.status_code=200
            return response
        else:
            return not_found()
    except Exception as e:
        	print(e)
    finally:
        cursor.close()
        conn.close()

#Altera informações de um produto específico
@app.route('/api/produtos/change', methods=['PUT'])
def atualiza_produto():
    try:
        _json = request.get_json(force = True)
        _json = request.json
        _id_produto = _json['id_produto']
        _nome_produto = _json['nome_produto']
        _preco_produto = _json['preco_produto']
        _desc_produto = _json['desc_produto']
        _status = _json['status']

        if _nome_produto and _preco_produto and _desc_produto and _status and _id_produto and request.method == 'PUT':
            sqlQuery = "UPDATE produtos.catalogo_produtos SET nome_produto=%s, preco_produto=%s, desc_produto=%s, status=%s WHERE id_produto=%s"
            bindData = (_nome_produto, _preco_produto, _desc_produto, _status, _id_produto,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto atualizado com sucesso!')
            response.status_code = 200
            return response
        else:
            return not_found()	
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
#Retorna todos os produtos
@app.route('/api/produtos', methods = ['GET'])
def retorna_produto():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ('SELECT * FROM produtos.catalogo_produtos')
        prodRows = cursor.fetchall()
        response = jsonify(prodRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#Retorna um produto específico
@app.route('/api/produtos/<int:id_produto>', methods=["GET"]) 
def retorna_produto_id(id_produto): 
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT  id_produto,nome_produto,desc_produto,status,preco_produto FROM produtos.catalogo_produtos WHERE id_produto =%s", id_produto)
        view_Rows = cursor.fetchone()
        if not view_Rows:
            return Response('Produto não cadastrado.'), 404
        response = jsonify(view_Rows)
        response.status_code = 200
        return response  
    except Exception as error:
        return jsonify({"error":f"{error}"}), 500
    finally:
        cursor.close() 
        conn.close()

@app.route("/api/produtos/healthcheck")
def hello():
    return "Ok."

@app.route('/api/produtos/swagger')
def get_docs():
    print('Preparando Swagger ...')
    return render_template('swaggerui.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5200)