import requests
import json


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

    
def vendite_giornaliere(data_inizio, data_fine):
    data = {
        "data_inizio": data_inizio,
        "data_fine": data_fine
    }

    try:
        response = requests.post(f"{base_url}/vendite_giornaliere", json=data, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Vendite trovate:")
                for vendita in result["vendite"]:
                    print(f"Filiale: {vendita['filiale']}, Data: {vendita['data_vendita']}, Tipo: {vendita['tipo']}, Veicolo: {vendita['veicolo']}")
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
    print("3. Cerca vendite")
    print("4. Esci")

    try:
        scelta = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue

    if scelta == 1:
        
        modello = input("Inserisci il modello dell'automobile: ")
        marca = input("Inserisci la marca dell'automobile: ")

        
        cerca_automobile(modello, marca)
    
    elif scelta == 2:
        modello = input("Inserisci il modello della moto: ")
        marca = input("Inserisci la marca della moto: ")

        
        cerca_motocicletta(modello, marca)

    elif scelta ==3:
        data_inizio = input("Inserisci la data di inizio (YYYY-MM-DD): ")
        data_fine = input("Inserisci la data di fine (YYYY-MM-DD): ")

        vendite_giornaliere(data_inizio, data_fine)

    elif scelta == 4:
        print("Arrivederci!")
        break

    else:
        print("Operazione non disponibile, riprova.")

