from flask import Flask, json, jsonify, request
api = Flask(__name__)


#mettere una lista di liste dove ogni lista è un cittadino

#la chiave è il codice fiscale
#add cittadino
#read cittadino
#update cittadino
#delete cittadino
cittadini={"dcfvfg70b34h501u": { 
    "nome": "Mario",
    "cognome" : "Garibaldi",
    "dataN" : "07/11/1890"}}

@api.route('/add_cittadino', methods=['POST'])


def GestisciAddCittadino():
    content_type = request.headers.get('Content-Type')
    print("chiamata Ricevuta" + 'application_type')
    if(content_type=='application/json'):
        jsonReq = request.json
        codice_fiscale = jsonReq.get('codFiscale')
        jsonResp={"Esito":"200", "Msg": "ok"}
        if codice_fiscale in cittadini:
            return jsonify({"Esito": "400", "Msg": "Cittadino già esistente"}), 400
        else:
            cittadini[codice_fiscale] = jsonReq
            return json.dumps(jsonResp)
        
        # if any(cittadino['codFiscale'] == codice_fiscale for cittadino in cittadini):
        #     return jsonify({"Esito": "400", "Msg": "Cittadino già esistente"}), 400
        # # Ecco un breve riepilogo di alcuni codici di stato HTTP comuni:
        # # 200 OK: La richiesta è stata elaborata con successo.
        # # 400 Bad Request: La richiesta non può essere elaborata a causa di un errore nel client (ad esempio, dati malformati).
        # # 404 Not Found: La risorsa richiesta non è stata trovata sul server.
        # # 500 Internal Server Error: Si è verificato un errore sul server durante l'elaborazione della richiesta.
    else:
        return 'Content-Type not supported!'
    


@api.route('/read_cittadino/<codice_fiscale>', methods=['GET'])
def read_cittadino():
    codice_fiscale= request.json
    cittadino = cittadini.get(codice_fiscale)
    if cittadino:
        return jsonify({"Esito" : "200", "Msg" : "cittadino trovato" + str(cittadino)}), 200

    else:
        return jsonify({"Esito": "200", "Msg": "Cittadino non trovato"}), 200

@api.route('/elimina_cittadino', methods=['POST'])
def elimina_cittadino():
    content_type = request.headers.get('Content-Type')
    print("chiamata Ricevuta" + 'application_type')
    if(content_type=='application/json'):
        cod = request.json
        jsonResp={"Esito":"200", "Msg": "errore cittadino non presente"}
        if cod in cittadini:
            del cittadini[cod]
            return jsonify({"Esito": "200", "Msg": "Cittadino rimosso con successo"}), 200
        else:
            
            return json.dumps(jsonResp)
        

api.run(host="127.0.0.1", port=8080)

