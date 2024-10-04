

import requests, json, sys


base_url = "https://192.168.174.64:8080"


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
    datiutente = {
        "user": user,
        "password": password
    }
    return datiutente


def GetCodicefiscale():
    cod = input('Inserisci codice fiscale: ')
    return {"codice fiscale": cod}

def Operazioni_cittadino():
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

        if sOper == 1 and privilegi == "w":
            print("Aggiunta cittadino")
            api_url = base_url + "/add_cittadino"
            jsonDataRequest = GetDatiCittadino()
            response = requests.post(api_url, json=jsonDataRequest, verify=False)

        elif sOper == 2:
            print("Richiesta dati cittadino")
            api_url = base_url + "/read_cittadino"
            jsonDataRequest = GetCodicefiscale()
            response = requests.post(api_url, json= jsonDataRequest, verify=False)
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
    if sOper==1:
        api_url = base_url + '/login_utente'
        jsonDataRequest = GetDatiAdmin()
        response = requests.post(api_url, json=jsonDataRequest, verify=False)
        jsonResp = response.json()
        esito=jsonResp["login"]
        if esito==True:
            Operazioni_cittadino()
            print(response.json())
            break
        else:
            print(response.json())
            print('riprova')
    elif sOper ==2:
        print("Buona giornata!")
        sys.exit()
    else:
            print("Operazione non disponibile, riprova.")

        
