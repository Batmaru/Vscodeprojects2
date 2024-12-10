import requests
import json
import sys


base_url = "https://127.0.0.1:8080"


def login():
    """Richiede le credenziali di accesso e verifica il login."""
    username = input("Inserisci username: ")
    password = input("Inserisci password: ")
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(f"{base_url}/login_utente", json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result.get("login"):
                return username, password  
            else:
                print(f"Errore nel login: {result.get('msg', 'Credenziali errate')}")
        else:
            print(f"Errore nella risposta del server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")
    return None, None




def cerca_casa_vendita(filiale, budget):
    """Cerca casa in vendita secondo i criteri forniti."""
    data = {
        "filiale": filiale,
        "budget": budget
    }
    try:
        response = requests.post(f"{base_url}/cerca_casa_vendita", json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Case trovate in vendita:")
                for casa in result["case"]:
                    print(f"catastale: {casa['catastale']},
                        indirizzo: {casa['indirizzo']},
                        numero_civico : {casa['numero_civico']},
                        piano : {casa['piano']},
                        prezzo: {casa['prezzo']}€,
                        superficie : {casa['superficie']} mq")
            else:
                print(f"Errore: {result.get('msg', 'Nessuna casa trovata')}")
        else:
            print(f"Errore nella risposta del server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")

def cerca_casa_affitto(prezzo_min, prezzo_max, indirizzo):
    """Cerca casa in affitto secondo i criteri forniti."""
    data = {
        "prezzomin": prezzo_min,
        "prezzomax": prezzo_max,
        "indirizzo": indirizzo
    }
    try:
        response = requests.post(f"{base_url}/cerca_casa_affitto", json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Case trovate in affitto:")
                for casa in result["case"]:
                    print(
                        f"Catastale: {casa['catastale']}, "
                        f"Indirizzo: {casa['indirizzo']}, "
                        f"Prezzo mensile: {casa['prezzo_mensile']}€, "
                        f"Tipo affitto: {casa['tipo_affitto']}"
                    )
            else:
                print(f"Errore: {result.get('msg', 'Nessuna casa trovata')}")
        else:
            print(f"Errore nella risposta del server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")

def vendi_casa(catastale, prezzo):
    """Registra una casa come venduta."""
    data = {
        "catastale": catastale,
        "prezzo": prezzo
    }
    try:
        response = requests.post(f"{base_url}/vendi_casa", json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Casa venduta con successo!")
            else:
                print(f"Errore: {result.get('msg', 'Errore durante la vendita')}")
        else:
            print(f"Errore nella risposta del server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")

def affitta_casa(catastale, prezzo_mensile):
    """Registra una casa come affittata."""
    data = {
        "catastale": catastale,
        "prezzo_mensile": prezzo_mensile  # Nome corretto
    }
    try:
        response = requests.post(f"{base_url}/affitta_casa", json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Casa affittata con successo!")
            else:
                print(f"Errore: {result.get('msg', 'Errore durante l\'affitto')}")
        else:
            print(f"Errore nella risposta del server: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")

import requests
import json

def richiedi_guadagni_filiali(server_url, data_inizio, data_fine, output_file="guadagni_filiali.json"):
    """
    Richiede i guadagni delle filiali al server e salva i risultati in un file JSON.
    
    :param server_url: URL del server (es. "http://localhost:5000/guadagni_filiali")
    :param data_inizio: Data di inizio del periodo (formato "YYYY-MM-DD").
    :param data_fine: Data di fine del periodo (formato "YYYY-MM-DD").
    :param output_file: Nome del file in cui salvare i risultati (default "guadagni_filiali.json").
    """
    payload = {
        "data_inizio": data_inizio,
        "data_fine": data_fine
    }

    try:
        
        response = requests.post(f"{server_url}/guadagni_filiali", json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
          
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data["guadagni"], f, ensure_ascii=False, indent=4)
                print(f"Guadagni salvati con successo in {output_file}")
            else:
                print(f"Errore dal server: {data.get('msg')}")
        else:
            print(f"Errore nella richiesta: {response.status_code}")
    except Exception as e:
        print(f"Errore durante la connessione al server: {str(e)}")



while True:
    print("\nOperazioni disponibili:")
    print("1. Login")
    print("2. Esci")

    try:
        Oper = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue

    if Oper == 1:
        username, password = login()
        if username and password:
            print("Accesso effettuato!")
            while True:
                print("\nOperazioni disponibili:")
                print("1. Cerca casa in vendita")
                print("2. Cerca casa in affitto")
                print("3. Vendi casa")
                print("4. Affitta casa")
                print("5. Statistiche di vendita e affito per filiale e guadagno")
                print("6. Esci")

                try:
                    scelta = int(input("Cosa vuoi fare? "))
                except ValueError:
                    print("Inserisci un numero valido!")
                    continue

                if scelta in [1, 2, 3, 4]:
                    
                        if scelta == 1:
                            prezzomin=input("Inserici il prezzo minimo")
                            prezzomax=input("inserisci il prezzo massimo")
                            indirizzo=input("inserisci la via")

                            cerca_casa_vendita(prezzomin, prezzomax, indirizzo)
                        elif scelta == 2:
                            prezzomin=input("Inserici il prezzo minimo")
                            prezzomax=input("inserisci il prezzo massimo")
                            indirizzo=input("inserisci la via")

                            cerca_casa_affitto()

                        elif scelta == 3:  
    
                            catastale = input("Inserisci il numero catastale della casa: ")
                            prezzo = input("Inserisci il prezzo di vendita: ")
                            vendi_casa(catastale, prezzo)

                        elif scelta==4:
                            catastale = input("Inserisci il numero catastale della casa: ")
                            canone_mensile = input("Inserisci il canone mensile effettivo: ")
                            affitta_casa(catastale, canone_mensile)
                        elif scelta ==5:
                            #dovevo implementare loperazione per i guadagni ma non ho tempoooo
                            break
                    
                elif scelta == 6:
                    print("Arrivederci!")
                    break
                else:
                    print("Operazione non disponibile, riprova.")
        else:
            print("Login fallito. Riprova.")

    elif Oper == 2:
        print("Buona giornata!")
        sys.exit()

    else:
        print("Operazione non disponibile, riprova.")
