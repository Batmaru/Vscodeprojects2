from flask import Flask,json,request
from myjson import *
import dbclient as db


api=Flask(__name__)
cur = db.connect()
if cur is None:
	print("Errore connessione al DB")
	sys.exit()

@api.route('/add_cittadino',methods=['POST'])
def GestisciAddCittadino():
    username=request.json["login"]["username"]
    password=request.json["login"]["password"]
    if Login(username,password)==True:
        dati = request.json["dati"]
        sQuery=f"insert into cittadini values('{dati['codice fiscale']}','{dati['nome']}','{dati['cognome']}','{dati['data nascita']}')"
        if db.write_in_db(cur,sQuery)==0:
            jsonResp = {"Esito":"200", "Msg":"cittadino aggiunto"}
            return json.dumps(jsonResp)
        elif db.write_in_db(cur,sQuery)==-2:
            jsonResp = {"Esito":"400", "Msg":"cittadino già esistente"}
            return json.dumps(jsonResp)
        else:
            jsonResp = {"Esito":"400", "Msg":"ERRORE"}
            return json.dumps(jsonResp)
    else:
        jsonResp = {"Esito":"400", "Msg":"diritti negati"}
        return json.dumps(jsonResp)

@api.route('/read_cittadino',methods=['POST'])
def GestisciReadCittadino():
    username=request.json["login"]["username"]
    password=request.json["login"]["password"]
    if Login(username,password)==True:
        cod=request.json["codF"]
        sQuery=f"select * from cittadini where cittadini.codicefiscale='{cod}'"
        if db.read_in_db(cur,sQuery)>0:
            """datiCittadino={}
            datiCittadino["nome"]=db.read_next_row(cur)[1][1]
            datiCittadino["cognome"]=db.read_next_row(cur)[1][2]
            datiCittadino["data di nascita"]=db.read_next_row(cur)[1][3] 
            """
            dati=[]
            for d in db.read_next_row(cur)[1]:
                dati.append(d)
            datiCittadino={}
            datiCittadino["nome"]=dati[1]
            datiCittadino["cognome"]=dati[2]
            datiCittadino["data di nascita"]=dati[3].strftime("%m/%d/%Y")
            jsonResp = {"Esito":"200", "Msg":"ok","Dati cittadino":datiCittadino}
            return json.dumps(jsonResp)
        else:
            jsonResp = {"Esito":"400", "Msg":"ERRORE"}
            return json.dumps(jsonResp)
    else:
        jsonResp = {"Esito":"400", "Msg":"diritti negati"}
        return json.dumps(jsonResp)

@api.route('/update_cittadino',methods=['POST'])
def GestisciUpdateCittadino():
    username=request.json["login"]["username"]
    password=request.json["login"]["password"]
    if Login(username,password)==True:
        dati=request.json["dati"]
        sQuery=f"update cittadini set nome='{dati['nome']}',cognome='{dati['cognome']}',datanascita='{dati['data nascita']}' where codicefiscale='{dati['codice fiscale']}'"
        if db.write_in_db(cur,sQuery)==0:
            jsonResp = {"Esito":"200", "Msg":"dati cittadino aggiornati"}
            return json.dumps(jsonResp)
        else:
            jsonResp = {"Esito":"400", "Msg":"ERRORE"}
            return json.dumps(jsonResp)
    else:
        jsonResp = {"Esito":"400", "Msg":"diritti negati"}
        return json.dumps(jsonResp)

@api.route('/delete_cittadino',methods=['POST'])
def GestisciDeleteCittadino():
    username=request.json["login"]["username"]
    password=request.json["login"]["password"]
    if Login(username,password)==True:
        cod=request.json["codF"]
        sQuery=f"delete from cittadini where codicefiscale='{cod}'"
        nQuery="select * from cittadini "
        ncitt=db.read_in_db(cur,nQuery)
        db.write_in_db(cur,sQuery)
        if ncitt>db.read_in_db(cur,nQuery):
            jsonResp = {"Esito":"200", "Msg":"dati cittadino rimossi correttamente"}
            return json.dumps(jsonResp)
        else:
            jsonResp = {"Esito":"400", "Msg":"ERRORE"}
            return json.dumps(jsonResp)
    else:
        jsonResp = {"Esito":"400", "Msg":"diritti negati"}
        return json.dumps(jsonResp)

@api.route('/login',methods=['POST'])
def GestisciLogin():
    utente=request.json  
    sQuery=f"select * from utenti where username='{utente['username']}' and password='{utente['password']}'"
    if db.read_in_db(cur,sQuery)>0:
        jsonResp={"Esito":"200", "Msg":"login effettuato correttamente","login":True,"privilegio":db.read_next_row(cur)[1][2]}
        return json.dumps(jsonResp)
    else:
        jsonResp = {"Esito":"402", "Msg":"username o password errati", "login":False}
        return json.dumps(jsonResp)

def Login(utente,password):
    sQuery=f"select * from utenti where username='{utente}'and password='{password}'"
    if db.read_in_db(cur,sQuery)>0: 
        return True
    else:
        return False

api.run(host="127.0.0.1", port=8080,ssl_context='adhoc')