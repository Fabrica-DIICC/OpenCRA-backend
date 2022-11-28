from __main__ import app, mysql, jsonify, request

@app.route("/alimentos", methods=["GET", "POST"])
def alimentos():
    cur = mysql.connection.cursor()
    lista_alimentos = []
    if request.method == 'GET':
        cur.execute("SELECT especie FROM alimento")
        #consulta
        _alimentos = cur.fetchall()
        for alimento in _alimentos:
            lista_alimentos.append(alimento[0])
        
    else:
        dict_alimentos = {}
        request_json = request.get_json()
        contaminantes = []
        if(request_json.get("contaminantes")):
            for contaminante in request_json.get("contaminantes"):
                contaminantes.append(contaminante)
            print(contaminantes)
            for contaminante in contaminantes:
                cur = mysql.connection.cursor()
                cur.execute("SELECT especie FROM alimento LEFT JOIN muestreo ON id_alimento=id_alimento LEFT JOIN contaminante ON contaminante.nombre = %s AND muestreo.cantidad != 0",[contaminante])
                _alimentos = cur.fetchall()
            for alimento in _alimentos:
                dict_alimentos[alimento[0]] = True

        lista_alimentos = dict_alimentos.keys

    return jsonify(lista_alimentos)
