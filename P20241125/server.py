
from flask import Flask, request, jsonify
import json
from dbclient import *
from datetime import datetime


api = Flask(__name__)

cur = connect()

@api.route('/login_utente', methods=['POST'])
def login_utente():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"login": False, "msg": "Dati mancanti"})

    # Modifica la query per leggere tutte le colonne o quelle richieste
    sql = f"SELECT id, username, nome, cognome, email FROM utenti WHERE username = '{username}' AND password = '{password}';"
    
    try:
        rows = read_in_db(cur, sql)

        if rows > 0:
            result = []
            for _ in range(rows):
                status, row = read_next_row(cur)
                if status == 0:
                    
                    result.append({
                        "id": row[0],
                        "username": row[1],
                        "nome": row[2],
                        "cognome": row[3],
                        "email": row[4],
                    })
            
            return jsonify({"login": True, "utente": result})
        else:
            return jsonify({"login": False, "msg": "Credenziali errate"})
    except Exception as e:
        return jsonify({"login": False, "msg": f"Errore: {str(e)}"})
@api.route('/cerca_automobile', methods=['POST'])
def cerca_automobile():

    data = request.json
    modello = data.get('modello').lower()
    marca = data.get('marca').lower()
    print(f"{modello},{marca}")
    cur = connect()

    query = f"""SELECT f.nome AS filiale, a.modello, a.marca, a.anno, a.disponibilita
    FROM automobili a, filiali f
    where f.id = a.filiale_id
    and LOWER(a.modello) = '{modello}' AND LOWER(a.marca) = '{marca}';
    """

    result = []

    try:
        rows_count = read_in_db(cur, query)  

        if rows_count > 0:
            
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:  
                    result.append({
                        'filiale': row[0],
                        'modello': row[1],
                        'marca': row[2],
                        'anno': row[3],
                        'disponibilita': row[4],
                    })
                else:
                    break  


            return jsonify({"success": True, "automobili": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna automobile trovata"})

    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})



@api.route('/cerca_motocicletta', methods=['POST'])
def cerca_motociletta():
    data = request.json
    modello = data.get('modello').lower()
    marca = data.get('marca').lower()
    
    cur=connect()

    query = f"""SELECT f.nome AS filiale, a.modello, a.marca, a.anno, a.disponibilita
    FROM motociclette a, filiali f
    where f.id = a.filiale_id
    and LOWER(a.modello) = '{modello}' AND LOWER(a.marca) = '{marca}';
    """

    result = []

    try:
        rows_count = read_in_db(cur, query)  

        if rows_count > 0:
            
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:  
                    result.append({
                        'filiale': row[0],
                        'modello': row[1],
                        'marca': row[2],
                        'anno': row[3],
                        'disponibilita': row[4]
                    })
                else:
                    break  

            return jsonify({"success": True, "moto": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna moto trovata"})

    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})
    
    

@api.route('/vendite_giornaliere', methods=['POST'])
def vendite_giornaliere():
    data = request.json
    data_inizio = data.get('data_inizio')
    data_fine = data.get('data_fine')
    
    cur=connect()
        
    query = f"""
    SELECT f.nome AS filiale, 
       v.data_vendita, 
       v.tipo, 
       CASE 
           WHEN v.tipo = 'automobile' THEN a.id  -- Prendi l'id dalla tabella automobili
           WHEN v.tipo = 'motocicletta' THEN m.id  -- Prendi l'id dalla tabella motociclette
       END AS veicolo_id,  -- Restituisce l'id del veicolo (auto o moto)
       CASE 
           WHEN v.tipo = 'automobile' THEN CONCAT(a.marca, ' ', a.modello)  -- Combina marca e modello per auto
           WHEN v.tipo = 'motocicletta' THEN CONCAT(m.marca, ' ', m.modello)  -- Combina marca e modello per moto
       END AS veicolo  -- Restituisce la descrizione del veicolo
    FROM venduti v
    JOIN filiali f ON v.filiale_id = f.id
    LEFT JOIN automobili a ON v.veicolo_id = a.id AND v.tipo = 'automobile'  -- Joins per le automobili
    LEFT JOIN motociclette m ON v.veicolo_id = m.id AND v.tipo = 'motocicletta'  -- Joins per le mo
    WHERE v.data_vendita BETWEEN '{data_inizio}' AND '{data_fine}';
    """


    result=[]

    if not data_inizio or not data_fine:
        return jsonify({"success": False, "msg": "Data inizio e data fine sono obbligatorie"})

    try:
        rows_count = read_in_db(cur, query) 


        if rows_count > 0:
            
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:  
                    result.append({ 
                    "filiale": row[0],
                    "data_vendita": row[1].strftime('%Y-%m-%d'),
                    "tipo": row[2],
                    "veicolo_id": row[3],
                    "veicolo": row[4],
                    
            })
                     
        file_path = 'vendite_giornaliere.json'
        with open(file_path, 'w') as json_file:
            json.dump({"vendite": result}, json_file, indent=4, default=str)

        if result:
            return jsonify({"success": True, "vendite": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna vendita trovata nel periodo specificato"})

    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})





if __name__ == '__main__':
    api.run(host="127.0.0.1", port=8080,ssl_context='adhoc')
    close(cur)


