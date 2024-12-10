
from flask import Flask, request, jsonify
from dbclient import *  
api = Flask(__name__)

cur = connect()

@api.route('/login_utente', methods=['POST'])
def login_utente():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"login": False, "msg": "Dati mancanti"})

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



@api.route('/cerca_casa_vendita', methods=['POST'])
def cerca_casa_vendita():
    data = request.json
    prezzo_min = data.get('prezzomin', 0)
    prezzo_max = data.get('prezzomax', 99999999)
    indirizzo = data.get('indirizzo', '').lower() 
    
    query = f"""
    SELECT catastale, indirizzo, prezzo, metri, stato
    FROM case_in_vendita
    WHERE prezzo BETWEEN {prezzo_min} AND {prezzo_max}
    AND LOWER(indirizzo) = LOWER('{indirizzo}');
    """
    
    try:
        rows_count = read_in_db(cur, query)
        result = []
        if rows_count > 0:
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:
                    result.append({
                        "catastale": row[0],
                        "indirizzo": row[1],
                        "prezzo": row[2],
                        "metri": row[3],
                        "stato": row[4],  
                    })
            return jsonify({"success": True, "case": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna casa trovata"})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})


@api.route('/cerca_casa_affitto', methods=['POST'])
def cerca_casa_affitto():
    """Cerca una casa in affitto in base al prezzo e indirizzo"""
    data = request.json
    prezzo_min = data.get('prezzomin', 0)
    prezzo_max = data.get('prezzomax', 99999999)
    indirizzo = data.get('indirizzo', '').lower() 
    
    query = f"""
    SELECT catastale, indirizzo, prezzo_mensile, tipo_affitto
    FROM case_in_affitto
    WHERE prezzo_mensile BETWEEN {prezzo_min} AND {prezzo_max}
    AND LOWER(indirizzo) LIKE LOWER('%{indirizzo}%');
    """
    
    try:
        rows_count = read_in_db(cur, query)
        result = []
        if rows_count > 0:
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:
                    result.append({
                        "catastale": row[0],
                        "indirizzo": row[1],
                        "prezzo_mensile": row[2],
                        "tipo_affitto": row[3],
                        "stato": row[4],
                    })
            return jsonify({"success": True, "case": result})
        else:
            return jsonify({"success": False, "msg": "Nessuna casa trovata"})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})
    

@api.route('/vendi_casa', methods=['POST'])
def vendi_casa():
    """Registra una casa come venduta."""
    data = request.json
    catastale = data.get('catastale')
    prezzo = data.get('prezzo')

    if not catastale or not prezzo:
        return jsonify({"success": False, "msg": "Dati mancanti"})

    try:
       
        query = f"""
        UPDATE case_in_vendita
        SET stato = 'venduta', prezzo_vendita = {prezzo}
        WHERE catastale = '{catastale}' AND stato = 'disponibile';
        """
        rows_updated = write_in_db(cur, query)

        if rows_updated > 0:
            return jsonify({"success": True, "msg": "Casa venduta con successo!"})
        else:
            return jsonify({"success": False, "msg": "Impossibile vendere la casa. Controlla i dati."})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})


@api.route('/affitta_casa', methods=['POST'])
def affitta_casa():
    """Registra una casa come affittata."""
    data = request.json
    catastale = data.get('catastale')
    prezzo_mensile = data.get('prezzo_mensile')  
    if not catastale or not prezzo_mensile:
        return jsonify({"success": False, "msg": "Dati mancanti"})

    try:
        
        query = f"""
        UPDATE case_in_affitto
        SET stato = 'affittata', prezzo_mensile_effettivo = {prezzo_mensile}
        WHERE catastale = '{catastale}' AND stato = 'disponibile';
        """
        rows_updated = write_in_db(cur, query)

        if rows_updated > 0:
            return jsonify({"success": True, "msg": "Casa affittata con successo!"})
        else:
            return jsonify({"success": False, "msg": "Impossibile affittare la casa. Controlla i dati."})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})
@api.route('/guadagni_filiali', methods=['POST'])
def guadagni_filiali():
    """Restituisce i guadagni delle filiali per un determinato periodo."""
    data = request.json
    data_inizio = data.get('data_inizio')
    data_fine = data.get('data_fine')

    if not data_inizio or not data_fine:
        return jsonify({"success": False, "msg": "Parametri data mancanti."})

    query = f"""
    SELECT
        f.partita_iva AS filiale,
        SUM(CASE 
            WHEN v.filiale_proponente = f.partita_iva THEN v.prezzo_vendita * 0.03
            ELSE v.prezzo_vendita * 0.01
        END) AS guadagno_vendite,
        COUNT(DISTINCT v.catastale) AS case_vendute,
        COUNT(DISTINCT a.catastale) AS case_affittate,
        COALESCE(SUM(a.durata_contratto * 500), 0) AS guadagno_affitti
    FROM filiali f
    LEFT JOIN vendite_casa v ON v.filiale_venditrice = f.partita_iva AND v.data_vendita BETWEEN '{data_inizio}' AND '{data_fine}'
    LEFT JOIN affitti_casa a ON a.filiale_venditrice = f.partita_iva AND a.data_affitto BETWEEN '{data_inizio}' AND '{data_fine}'
    GROUP BY f.partita_iva;
    """
    
    try:
        rows_count = read_in_db(cur, query)
        result = []
        if rows_count > 0:
            for _ in range(rows_count):
                status, row = read_next_row(cur)
                if status == 0:
                    result.append({
                        "filiale": row[0],
                        "guadagno_vendite": float(row[1] or 0),
                        "case_vendute": int(row[2] or 0),
                        "case_affittate": int(row[3] or 0),
                        "guadagno_affitti": float(row[4] or 0),
                        "guadagno_totale": float((row[1] or 0) + (row[4] or 0)),
                    })
            return jsonify({"success": True, "guadagni": result})
        else:
            return jsonify({"success": False, "msg": "Nessun guadagno trovato nel periodo specificato"})
    except Exception as e:
        return jsonify({"success": False, "msg": f"Errore: {str(e)}"})


if __name__ == '__main__':
    api.run(host="127.0.0.1", port=8080, ssl_context='adhoc')
    close(cur)
