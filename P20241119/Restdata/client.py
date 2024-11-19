import requests
from requests.auth import HTTPBasicAuth
import json
import sys

base_url = "https://127.0.0.1:8080"

def GetDatiCittadino():
    nome = input("Inserisci il nome: ")
    cognome = input("Inserisci il cognome: ")
    dataN = input("Inserisci la data di nascita (gg/mm/aaaa): ")
    codF = input("Inserisci il codice fiscale: ")
    datiCittadino = {
        "nome": nome, 
        "cognome": cognome, 
        "data nascita": dataN, 
        "codice fiscale": codF
    }
    return datiCittadino

def GetCodicefiscale():
    cod = input('Inserisci codice fiscale: ')
    return {"codice fiscale": cod}

def GetAuthCredentials():
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")
    return username, password

def CheckLogin():
    """Verifica le credenziali prima di ogni operazione."""
    username, password = GetAuthCredentials()
    api_url = base_url + '/login_utente'
    jsonDataRequest = {"user": username, "password": password}
    try:
        response = requests.post(api_url, json=jsonDataRequest, verify=False)
        response.raise_for_status()
        jsonResp = response.json()
        if jsonResp.get("login"):
            return username, password
        else:
            print("Credenziali errate. Riprova.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Errore durante il controllo delle credenziali: {e}")
        return None, None

def Operazioni(privilegi):
    while True:
        print("\nOperazioni disponibili:")
        if privilegi == 'r':
            print("2. Richiedi cittadino")
            print("5. Esci")
        elif privilegi == 'w':
            print("1. Inserisci cittadino")
            print("2. Richiedi cittadino")
            print("3. Modifica cittadino")
            print("4. Elimina cittadino")
            print("5. Esci")

        try:
            sOper = int(input("Cosa vuoi fare? "))
        except ValueError:
            print("Inserisci un numero valido!")
            continue

        if privilegi == 'r' and sOper != 2:
            print("Non hai il permesso di eseguire questa operazione.")
            continue

        # Verifica login prima di ogni operazione
        username, password = CheckLogin()
        if not username or not password:
            print("Accesso negato. Torna al menu.")
            continue

        # Operazioni disponibili
        if sOper == 1 and privilegi == 'w':
            print("Aggiunta cittadino")
            api_url = base_url + "/add_cittadino"
            jsonDataRequest = GetDatiCittadino()
            response = requests.post(api_url, json=jsonDataRequest, auth=HTTPBasicAuth(username, password), verify=False)
            print(response.json())

        elif sOper == 2:
            print("Richiesta dati cittadino")
            api_url = base_url + "/read_cittadino"
            jsonDataRequest = GetCodicefiscale()
            response = requests.post(api_url, json=jsonDataRequest, auth=HTTPBasicAuth(username, password), verify=False)
            print(response.json())

        elif sOper == 3 and privilegi == 'w':
            print("Modifica cittadino")
            api_url = base_url + "/update_cittadino"
            jsonDataRequest = GetDatiCittadino()
            response = requests.post(api_url, json=jsonDataRequest, auth=HTTPBasicAuth(username, password), verify=False)
            print(response.json())

        elif sOper == 4 and privilegi == 'w':
            print("Eliminazione cittadino")
            api_url = base_url + "/elimina_cittadino"
            jsonDataRequest = GetCodicefiscale()
            response = requests.post(api_url, json=jsonDataRequest, auth=HTTPBasicAuth(username, password), verify=False)
            print(response.json())

        elif sOper == 5:
            print("Buona giornata!")
            sys.exit()

        else:
            print("Operazione non disponibile, riprova.")


while True:
    print("\nOperazioni disponibili:")
    print('1. login utente')
    print('2. esci')

    try:
        sOper = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue

    if sOper == 1:
        api_url = base_url + '/login_utente'
        username, password = GetAuthCredentials()
        
        jsonDataRequest = {"user": username, "password": password}
        
        try:
            response = requests.post(api_url, json=jsonDataRequest, verify=False)
            response.raise_for_status()  # Verifica se la richiesta ha avuto successo (es. status code 200)
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta: {e}")
            continue

        try:
            jsonResp = response.json()
        except ValueError:
            print("Errore di decodifica JSON. Controlla la risposta del server.")
            print("Response text:", response.text)
            continue

        esito = jsonResp.get("login")
        privilegi = jsonResp.get("privilegi")

        if esito:
            print("Login effettuato con successo!")
            Operazioni(privilegi)  # Passa solo privilegi alla funzione
            break
        else:
            print("Errore di login: ", jsonResp.get("Msg"))
            print('Riprova')
    elif sOper == 2:
        print("Buona giornata!")
        sys.exit()
    else:
        print("Operazione non disponibile, riprova.")
