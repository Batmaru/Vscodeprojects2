import requests,json,sys

base_url="https://127.0.0.1:8080"

def GetDatiCittadino():
    nome = input("Inserisci nome: ")
    cognome = input("Inserisci cognome: ")
    dataN = input("Inserisci data di nascita: ")
    codF = input("Inserisci codice fiscale: ")
    datiCittadino = {"nome":nome, "cognome": cognome, "data nascita":dataN, "codice fiscale":codF}
    return datiCittadino

def GetCodiceFiscale():
    cod=input("Inserisci codice fiscale: ")
    return cod

def Login():
    username=input("Inserisci username: ")
    password=input("Inserisci password: ")
    return {"username":username,"password":password}


while True:
    print("\nOperazioni disponibili:")
    print("1. Login")
    print("2. Esci")

    try:
        Oper = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue

    if Oper==1:
        api_url = base_url + "/login"
        jsonDataRequest = Login()
        response = requests.post(api_url,json=jsonDataRequest, verify=False)
        print(response.json())

        if response.json()["login"]==True:
            
            username=jsonDataRequest["username"]
            password=jsonDataRequest["password"]
            jsonDatiLogin={"username":username,"password":password}
            if response.json()["privilegio"]=="w":
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
                    if sOper==1:
                        api_url = base_url + "/add_cittadino"
                        jsonDataRequest = GetDatiCittadino()
                        response = requests.post(api_url,json={"login":jsonDatiLogin,"dati":jsonDataRequest}, verify=False)
                        data1 = response.json()
                        print(data1)
                    elif sOper==2:
                        api_url=base_url+"/read_cittadino"
                        jsonDataRequest = GetCodiceFiscale()
                        response = requests.post(api_url,json={"login":jsonDatiLogin,"codF":jsonDataRequest}, verify=False)
                        print(response.json())
                    elif sOper==3:
                        api_url=base_url+"/update_cittadino"
                        jsonDataRequest = GetDatiCittadino()
                        response = requests.post(api_url,json={"login":jsonDatiLogin,"dati":jsonDataRequest}, verify=False)
                        print(response.json())
                    elif sOper==4:
                        api_url=base_url+"/delete_cittadino"
                        jsonDataRequest = GetCodiceFiscale()
                        response = requests.post(api_url,json={"login":jsonDatiLogin,"codF":jsonDataRequest}, verify=False)
                        print(response.json())
                    elif sOper==5:
                        sys.exit()

            elif response.json()["privilegio"]=="r":
                while True:
                    print("\nOperazioni disponibili:")
                    print("1. Richiedi cittadino")
                    print("2. Esci")

                    try:
                        sOper = int(input("Cosa vuoi fare? "))
                    except ValueError:
                        print("Inserisci un numero valido!")
                        continue
                    if sOper==1:
                        api_url=base_url+"/read_cittadino"
                        jsonDataRequest = GetCodiceFiscale()
                        response = requests.post(api_url,json={"login":jsonDatiLogin,"codF":jsonDataRequest}, verify=False)
                        print(response.json())
                    elif sOper==2:
                        sys.exit()
    elif Oper==2:
        sys.exit()