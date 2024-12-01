import requests
import json

# URL del server Flask
base_url = "https://127.0.0.1:8080"

def cerca_automobile(modello, marca):
    data = {
        "modello": modello,
        "marca": marca
    }

    try:
        response = requests.post(f"{base_url}/cerca_automobile", json=data, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Automobili trovate:")
                for auto in result["automobili"]:
                    print(f"Filiale: {auto['filiale']}, Modello: {auto['modello']}, Marca: {auto['marca']}, Anno: {auto['anno']}, Disponibilità: {auto['disponibilita']}")
            else:
                print(f"Errore: {result.get('msg', 'Errore sconosciuto')}")
        else:
            print(f"Errore nella risposta: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")



def cerca_motocicletta(modello, marca):
    data = {
        "modello": modello,
        "marca": marca
    }

    try:
        response = requests.post(f"{base_url}/cerca_motocicletta", json=data, verify=False)
        if response.status_code==200:
            result = response.json
            result = response.json()
            if result["success"]:
                print("moto trovate:")
                for moto in result["moto"]:
                    print(f"Filiale: {moto['filiale']}, Modello: {moto['modello']}, Marca: {moto['marca']}, Anno: {moto['anno']}, Disponibilità: {moto['disponibilita']}")
            else:
                print(f"Errore: {result.get('msg', 'Errore sconosciuto')}")
        else:
            print(f"Errore nella risposta: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")


while True:
    print("\nOperazioni disponibili:")
    print("1. Cerca automobile")
    print("2. Cerca moto")
    print("3. Esci")

    try:
        scelta = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue

    if scelta == 1:
        # Chiedi all'utente di inserire marca e modello
        modello = input("Inserisci il modello dell'automobile: ")
        marca = input("Inserisci la marca dell'automobile: ")

        # Esegui la ricerca
        cerca_automobile(modello, marca)
    
    elif scelta == 2:
        modello = input("Inserisci il modello della moto: ")
        marca = input("Inserisci la marca della moto: ")

        
        cerca_motocicletta(modello, marca)

    elif scelta == 3:
        print("Arrivederci!")
        break

    else:
        print("Operazione non disponibile, riprova.")

