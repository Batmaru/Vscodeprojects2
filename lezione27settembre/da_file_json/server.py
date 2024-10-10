from flask import Flask, jsonify, request
from myjson import JsonDeserialize, JsonSerialize

api = Flask(__name__)

file_path = "anagrafe.json"
utenti_path = "utenti.json"
cittadini = JsonDeserialize(file_path)
utenti = JsonDeserialize(utenti_path)

def verify_credentials(username, password):
    user = utenti.get(username)
    if user and user['password'] == password:
        return True
    return False

def verify_user_privileges(username):
    user = utenti.get(username)
    if user:
        return user['privileges']
    return None

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():
    auth = request.authorization
    if not auth or not verify_credentials(auth.username, auth.password):
        return jsonify({"Esito": "401", "Msg": "Unauthorized access"}), 401
    
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

@api.route('/read_cittadino', methods=['POST'])
def GestisciReadCittadino():
    auth = request.authorization
    if not auth or not verify_credentials(auth.username, auth.password):
        return jsonify({"Esito": "401", "Msg": "Unauthorized access"}), 401

    cod = request.json.get("codice fiscale")
    if cod in cittadini:
        jsonResp = {"Esito": "200", "Msg": "ok", "Dati cittadino": cittadini[cod]}
        return jsonify(jsonResp)
    else:
        jsonResp = {"Esito": "200", "Msg": "Cittadino non presente"}
        return jsonify(jsonResp)

@api.route('/update_cittadino', methods=['POST'])
def update_cittadino():
    auth = request.authorization
    if not auth or not verify_credentials(auth.username, auth.password):
        return jsonify({"Esito": "401", "Msg": "Unauthorized access"}), 401

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codice fiscale')
        if codice_fiscale in cittadini:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path)
            return jsonify({"Esito": "200", "Msg": "Cittadino aggiornato con successo"})
        else:
            return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"}), 404
    else:
        return 'Content-Type non supportato!'

@api.route('/elimina_cittadino', methods=['POST'])
def elimina_cittadino():
    auth = request.authorization
    if not auth or not verify_credentials(auth.username, auth.password):
        return jsonify({"Esito": "401", "Msg": "Unauthorized access"}), 401

    cod = request.json.get('codice fiscale')
    if cod in cittadini:
        del cittadini[cod]
        JsonSerialize(cittadini, file_path)
        return jsonify({"Esito": "200", "Msg": "Cittadino rimosso con successo"}), 200
    else:
        return jsonify({"Esito": "200", "Msg": "Cittadino non trovato"}), 200

@api.route('/login_utente', methods=['POST'])
def login():
    user_utente = request.json.get('user')
    password = request.json.get('password')
    if user_utente in utenti:
        user_info = utenti[user_utente]
        if user_info["password"] == password:
            return jsonify({"Esito": "200", "Msg": "Login effettuato con successo", "login": True, "privilegi": user_info["privilegi"]}), 200
        else:
            return jsonify({"Esito": "200", "Msg": "Password errata", "login": False}), 200
    else:
        return jsonify({"Esito": "200", "Msg": "User non esistente", "login": False}), 200



# api.run(host="127.0.0.1", port=8080)
api.run(host="172.24.79.117", port=8080, ssl_context="adhoc")