from flask import Flask, jsonify, request, json
from myjson import JsonDeserialize, JsonSerialize

api = Flask(__name__)


file_path = "anagrafe.json"
cittadini = JsonDeserialize(file_path)

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codice fiscale')
        if codice_fiscale in cittadini:
            return jsonify({"Esito": "200", "Msg": "Cittadino già esistente"}), 200
        else:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path) 
            return jsonify({"Esito": "200", "Msg": "Cittadino aggiunto con successo"}), 200
    else:
        return 'Content-Type non supportato!'
    
@api.route('/read_cittadino',methods=['POST'])
def GestisciReadCittadino():
    cod=request.json
    for c in cittadini:
        if cod==c:
            jsonResp = {"Esito":"200", "Msg":"ok","Dati cittadino":cittadini[c]}
            return json.dumps(jsonResp)
    jsonResp = {"Esito":"200", "Msg":"cittadino non presente"}
    return json.dumps(jsonResp)


def update_cittadino():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codice fiscale')
        if codice_fiscale in cittadini:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path)  
            return json.dumps({"Esito": "200", "Msg": "Cittadino aggiornato con successo"})
        else:
            return json.dumps({"Esito": "404", "Msg": "Cittadino non trovato"}), 404
    else:
        return 'Content-Type non supportato!'

@api.route('/elimina_cittadino', methods=['POST'])
def elimina_cittadino():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        cod = request.json.get('codice fiscale')
        if cod in cittadini:
            del cittadini[cod]
            JsonSerialize(cittadini, file_path)  
            return jsonify({"Esito": "200", "Msg": "Cittadino rimosso con successo"}), 200
        else:
            return jsonify({"Esito": "200", "Msg": "Cittadino non trovato"}), 200
    else:
        return 'Content-Type non supportato!'
    
    
@api.route('/login_cittadino', methods=['POST'])
def login():
    dictpersona=request.json
    codf=dictpersona['codice fiscale']
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        for k,v in cittadini.items():
            if k==codf:
                if v['nome']== dictpersona['nome']:
                    if v['cognome']==dictpersona['cognome']:
                        if v['data nascita']==dictpersona['data nascita']:
                            if v['codice fiscale']==dictpersona['codice fiscale']:
                                return jsonify({"Esito": "200", "Msg": "Controlli andati a buon fine"}), 200
                            else:
                                return jsonify({"Esito": "200", "Msg": "Codice fiscale non corretto"}), 200
                        else:
                            return jsonify({"Esito": "200", "Msg": "Data di nascita non corretta"}), 200
                    else:
                        return jsonify({"Esito": "200", "Msg": "Cognome non corretto"}), 200
                else:
                    return jsonify({"Esito": "200", "Msg": "Nome non corretto"}), 200
        
        return jsonify({"Esito": "200", "Msg": "Codice fiscale non corretto"}), 200
    else:
        return 'Content-Type non supportato!'

api.run(host="127.0.0.1", port=8080)

