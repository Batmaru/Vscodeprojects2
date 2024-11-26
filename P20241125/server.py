from flask import Flask, request, jsonify
import json
from dbclient import *
from datetime import datetime

api = Flask(__name__)

cur =connect()


@api.route('/cerca_automobile', methods=['POST'])
def cerca_automobile():
    data= request.json
    modello= data.get('modello')
    marca = data.get('marca')

    
    cur = connect()

    # Definisci la query
    query = """
    SELECT f.nome AS filiale, a.modello, a.marca, a.anno, a.disponibilita
    FROM automobili a, filiali f
    WHERE f.id = a.filiale_id
    AND a.modello = %s AND a.marca = %s"""
    
  
    result = []

    try:
       
        rows_count = read_in_db(cur, query)
        
        
        if rows_count > 0:
            
            cur.execute(query, (modello, marca))
            
            
            while True:
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
        return jsonify({"success": False, "msg": str(e)})


if __name__ == '__main__':
    api.run(host="127.0.0.1", port=8080,ssl_context='adhoc')
    close(cur)
