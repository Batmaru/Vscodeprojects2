from flask import Flask, jsonify, request
from myjson import JsonDeserialize, JsonSerialize

api = Flask(__name__)

file_path = "anagrafe.json"
cittadini = JsonDeserialize(file_path)

file_path1 = "utenti.json"
admin = JsonDeserialize(file_path1)

# Funzione per verificare le credenziali utente
def verifica_utente(user, password):
    if user in admin and admin[user]["password"] == password:
        return True
    return False

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():
    if verifica_utente(request.json.get('user'), request.json.get('password')):
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codice fiscale')
        if codice_fiscale in cittadini:
            return jsonify({"Esito": "200", "Msg": "Cittadino già esistente"}), 200
        else:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path)
            return jsonify({"Esito": "200", "Msg": "Cittadino aggiunto con successo"}), 200
    return jsonify({"Esito": "403", "Msg": "Autenticazione fallita"}), 403

@api.route('/read_cittadino', methods=['POST'])
def GestisciReadCittadino():
    if verifica_utente(request.json.get('user'), request.json.get('password')):
        cod = request.json.get('codice fiscale')
        if cod in cittadini:
            return jsonify({"Esito":"200", "Msg":"ok", "Dati cittadino": cittadini[cod]})
        return jsonify({"Esito":"200", "Msg":"Cittadino non presente"})
    return jsonify({"Esito": "403", "Msg": "Autenticazione fallita"}), 403

@api.route('/update_cittadino', methods=['POST'])
def update_cittadino():
    if verifica_utente(request.json.get('user'), request.json.get('password')):
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codice fiscale')
        if codice_fiscale in cittadini:
            cittadini[codice_fiscale] = jsonReq
            JsonSerialize(cittadini, file_path)
            return jsonify({"Esito": "200", "Msg": "Cittadino aggiornato con successo"}), 200
        return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"}), 404
    return jsonify({"Esito": "403", "Msg": "Autenticazione fallita"}), 403

@api.route('/elimina_cittadino', methods=['POST'])
def elimina_cittadino():
    if verifica_utente(request.json.get('user'), request.json.get('password')):
        cod = request.json.get('codice fiscale')
        if cod in cittadini:
            del cittadini[cod]
            JsonSerialize(cittadini, file_path)
            return jsonify({"Esito": "200", "Msg": "Cittadino rimosso con successo"}), 200
        return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"}), 404
    return jsonify({"Esito": "403", "Msg": "Autenticazione fallita"}), 403

@api.route('/login_utente', methods=['POST'])
def login():
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


#api.run(host="192.168.174.64", port=8080, ssl_context="adhoc")
api.run(host="192.168.173.95", port=8080, ssl_context="adhoc")
