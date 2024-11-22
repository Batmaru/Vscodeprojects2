from flask import Flask, request, jsonify
import json
from dbclient import connect, write_in_db, read_in_db, read_next_row, close
from datetime import datetime

app = Flask(__name__)

cur =connect()

@app.route('/login_utente', methods=['POST'])
def login_utente():
    data = request.json
    username = data.get("user")
    password = data.get("password")

    if not username or not password:
        return jsonify({"login": False, "Msg": "Dati mancanti"})

    sql = f"SELECT privilegi FROM utenti WHERE username = '{username}' AND password = '{password}';"
    rows = read_in_db(cur, sql)

    if rows > 0:
        _, result = read_next_row(cur)
        privilegi = result[0]
        return jsonify({"login": True, "privilegi": privilegi})
    else:
        return jsonify({"login": False, "Msg": "Credenziali errate"})


@app.route('/add_cittadino', methods=['POST'])
def add_cittadino():
    data = request.json
    nome = data.get("nome")
    cognome = data.get("cognome")
    data_nascita = data.get("data nascita")
    codice_fiscale = data.get("codice fiscale")

    if not all([nome, cognome, data_nascita, codice_fiscale]):
        return jsonify({"Esito": "400", "Msg": "Dati mancanti"})

    try:
        data_nascita = datetime.strptime(data_nascita, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({"Esito": "400", "Msg": "Formato data errato"})

    sql = f"""
    INSERT INTO anagrafe (nome, cognome, data_nascita, codice_fiscale)
    VALUES ('{nome}', '{cognome}', '{data_nascita}', '{codice_fiscale}');
    """
    result = write_in_db(cur, sql)

    if result == 0:
        return jsonify({"Esito": "200", "Msg": "Cittadino aggiunto con successo"})
    elif result == -2:
        return jsonify({"Esito": "400", "Msg": "Codice fiscale duplicato"})
    else:
        return jsonify({"Esito": "500", "Msg": "Errore del server"})


@app.route('/read_cittadino', methods=['POST'])
def read_cittadino():
    data = request.json
    codice_fiscale = data.get("codice fiscale")

    if not codice_fiscale:
        return jsonify({"Esito": "400", "Msg": "Codice fiscale mancante"})

    sql = f"SELECT nome, cognome, data_nascita, codice_fiscale FROM anagrafe WHERE codice_fiscale = '{codice_fiscale}';"
    rows = read_in_db(cur, sql)

    if rows > 0:
        _, result = read_next_row(cur)
        return jsonify({
            "Esito": "200",
            "Dati": {
                "nome": result[0],
                "cognome": result[1],
                "data nascita": result[2],
                "codice fiscale": result[3]
            }
        })
    else:
        return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"})

@app.route('/update_cittadino', methods=['POST'])
def update_cittadino():
    data = request.json
    nome = data.get("nome")
    cognome = data.get("cognome")
    data_nascita = data.get("data nascita")
    codice_fiscale = data.get("codice fiscale")

    if not all([nome, cognome, data_nascita, codice_fiscale]):
        return jsonify({"Esito": "400", "Msg": "Dati mancanti"})

    try:
        data_nascita = datetime.strptime(data_nascita, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({"Esito": "400", "Msg": "Formato data errato"})

    sql = f"""
    UPDATE anagrafe
    SET nome = '{nome}', cognome = '{cognome}', data_nascita = '{data_nascita}'
    WHERE codice_fiscale = '{codice_fiscale}';
    """
    result = write_in_db(cur, sql)

    if result == 0:
        return jsonify({"Esito": "200", "Msg": "Cittadino aggiornato con successo"})
    else:
        return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"})

@app.route('/elimina_cittadino', methods=['POST'])
def elimina_cittadino():
    data = request.json
    codice_fiscale = data.get("codice fiscale")

    if not codice_fiscale:
        return jsonify({"Esito": "400", "Msg": "Codice fiscale mancante"})

    sql = f"DELETE FROM anagrafe WHERE codice_fiscale = '{codice_fiscale}';"
    result = write_in_db(cur, sql)

    if result == 0:
        return jsonify({"Esito": "200", "Msg": "Cittadino eliminato con successo"})
    else:
        return jsonify({"Esito": "404", "Msg": "Cittadino non trovato"})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080,ssl_context='adhoc')
    close(cur)
