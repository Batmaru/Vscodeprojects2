
from flask import Flask, request, jsonify
import json
from dbclient import *
from datetime import datetime

api = Flask(__name__)

cur = connect()

@api.route('/cerca_automobile', methods=['POST'])
def cerca_automobile():

    data = request.json
    modello = data.get('modello').lower()
    marca = data.get('marca').lower()

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
                        'disponibilita': row[4]
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
    SELECT f.nome AS filiale, v.data_vendita, v.tipo, 
           CASE 
               WHEN v.tipo = 'automobile' THEN (SELECT CONCAT(a.marca, ' ', a.modello) FROM automobili a WHERE a.id = v.item_id)
               WHEN v.tipo = 'motocicletta' THEN (SELECT CONCAT(m.marca, ' ', m.modello) FROM motociclette m WHERE m.id = v.item_id)
           END AS veicolo
    FROM venduti v
    JOIN filiali f ON v.filiale_id = f.id
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
                    "veicolo": row[3]
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


