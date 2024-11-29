
from flask import Flask, request, jsonify
import json
from dbclient import *
from datetime import datetime

api = Flask(__name__)

cur = connect()

@api.route('/cerca_automobile', methods=['POST'])
def cerca_automobile():
    data = request.json
    modello = data.get('modello', '').strip()
    marca = data.get('marca', '').strip()

    cur = connect()

    query = """
    SELECT f.nome AS filiale, a.modello, a.marca, a.anno, a.disponibilita
    FROM automobili a, filiali f
    where f.id = a.filiale_id
    and a.modello = '%s' AND a.marca = '%s';
    """ % (modello, marca)  

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
                    break  ì

            return jsonify({"success": True, "automobili": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna automobile trovata"})

    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})

if __name__ == '__main__':
    api.run(host="127.0.0.1", port=8080,ssl_context='adhoc')
    close(cur)