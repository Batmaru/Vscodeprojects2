import json
import requests
import sys

base_url = "https://192.168.173.95:8080"

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

def GetDatiAdmin():
    user = input("Inserisci l'username: ")
    password = input("Inserisci la password: ")
    return {"user": user, "password": password}

def GetCodicefiscale():
    cod = input('Inserisci codice fiscale: ')
    return {"codice fiscale": cod}

def verifica_utente(user, password):
    with open('utenti.json', 'r') as file:
        utenti = json.load(file)

    for utente in utenti:
        if utente['user'] == user and utente['password'] == password:
            return utente.get('privilegi', None)  # Restituisci i privilegi se l'utente è trovato
    return None

def Operazioni_cittadino(user, password, privilegi):
    while True:
        print("\nOperazioni disponibili:")
        if privilegi == "w":
            print("1. Inserisci cittadino")
            print("2. Richiedi cittadino")
            print("3. Modifica cittadino")
            print("4. Elimina cittadino")
        elif privilegi == "r":
            print("2. Richiedi cittadino")

        print("5. Esci")

        try:
            sOper = int(input("Cosa vuoi fare? "))
        except ValueError:
            print("Inserisci un numero valido!")
            continue

        # Verifica delle credenziali
        if verifica_utente(user, password) is None:
            print("Autenticazione fallita. Controlla le credenziali.")
            continue  # Torna all'inizio del ciclo se le credenziali non sono corrette

        if sOper == 1 and privilegi == "w":
            print("Aggiunta cittadino")
            api_url = base_url + "/add_cittadino"
            jsonDataRequest = GetDatiCittadino()  
            response = requests.post(api_url, json=jsonDataRequest, verify=False)
            print(response.json())

        elif sOper == 2:
            print("Richiesta dati cittadino")
            api_url = base_url + "/read_cittadino"
            jsonDataRequest = GetCodicefiscale()
            response = requests.post(api_url, json=jsonDataRequest, verify=False)
            print(response.json())

        elif sOper == 3 and privilegi == "w":
            print("Modifica cittadino")
            api_url = base_url + "/update_cittadino"
            jsonDataRequest = GetDatiCittadino()  
            response = requests.post(api_url, json=jsonDataRequest, verify=False)
            print(response.json())

        elif sOper == 4 and privilegi == "w":
            print("Eliminazione cittadino")
            api_url = base_url + "/elimina_cittadino"
            jsonDataRequest = GetCodicefiscale()  
            response = requests.post(api_url, json=jsonDataRequest, verify=False)
            print(response.json())

        elif sOper == 5:
            print("Buona giornata!")
            sys.exit()

        else:
            print("Operazione non disponibile o privilegi insufficienti, riprova.")

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
        jsonDataRequest = GetDatiAdmin()
        privilegi = verifica_utente(jsonDataRequest['user'], jsonDataRequest['password'])

        if privilegi:
            print("Login effettuato con successo!")
            Operazioni_cittadino(jsonDataRequest['user'], jsonDataRequest['password'], privilegi)
            break
        else:
            print("Errore di login: credenziali non valide.")
            print('Riprova')
    elif sOper == 2:
        print("Buona giornata!")
        sys.exit()
    else:
        print("Operazione non disponibile, riprova.")
