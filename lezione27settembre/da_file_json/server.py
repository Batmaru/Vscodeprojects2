from flask import Flask, jsonify, request, json
from myjson import JsonDeserialize, JsonSerialize

api = Flask(__name__)


file_path = "anagrafe.json"
cittadini = JsonDeserialize(file_path)
file_path1="utenti.json"
admin=JsonDeserialize(file_path1)

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
    
    
@api.route('/login_utente', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        user_utente = request.json.get('user')
        password = request.json.get('password')
        if user_utente in admin:
            user_info = admin[user_utente]
            if user_info["password"] == password:
                return jsonify({"Esito": "200", "Msg": "Login effettuato con successo", "login": True, "privilegi": user_info["privilegi"]}), 200
            else:
                return jsonify({"Esito": "200", "Msg": "Password errata", "login": False}), 200
        else:
            return jsonify({"Esito": "200", "Msg": "User non esistente", "login": False}), 200
    else:
        return 'Content-Type non supportato!'
    


api.run(host="192.168.174.64", port=8080, ssl_context="adhoc")

