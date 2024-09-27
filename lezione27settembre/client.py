import requests, json, sys
base_url = "http://127.0.0.1:8080"


def GetDatiCittadino():
    nome = "Mario"
    cognome = "Garibaldi"
    dataN = "07/11/1890"
    codF = "dcfvfg70b34h501u"
    datiCittadino = {"nome":nome, "cognome": cognome, "dataNascita":dataN, "codFiscale":codF}
    return datiCittadino

def GetCodicefiscale():
    cod=input('inserisci codice fiscale: ')
    return cod

    
while True:
    print("\nOperazioni disponibili:")
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

    if sOper == 1:
        print("richiesto aggiungi cittadino")
        api_url = base_url + "/add_cittadino"
        jsonDataRequest = GetDatiCittadino()
        response = requests.post(api_url,json=jsonDataRequest)

    elif sOper == 2:
        print("richiesta dei dati del cittadino")
        api_url = base_url + "/read_cittadino"
        jsonDataRequest = GetCodicefiscale()
        response = requests.post(api_url,json=jsonDataRequest)
    elif sOper ==4:
        print("richiesta di eliminazione del cittadino")
        api_url = base_url + "/elimina_cittadino"
        jsonDataRequest = GetCodicefiscale()
        response = requests.post(api_url,json=jsonDataRequest)

    elif sOper == 5:
        print("Buona giornata!")
        sys.exit()
    else:
        print("Operazione non disponibile, riprova.")
        
   






api_url = base_url + "/add_cittadino"
jsonDataRequest = GetDatiCittadino()
response = requests.post(api_url,json=jsonDataRequest)
#print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])
data1 = response.json()
print(data1)

