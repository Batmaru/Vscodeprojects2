import os
import csv
from flask import Flask, render_template, request

api = Flask(__name__)

# Percorso del file CSV dove memorizzare gli utenti registrati
file_utenti = "utenti_registrati.csv"

# Funzione per salvare i dati nel file CSV
def salva_dati_utente(nome, cognome, password, sesso):
    with open(file_utenti, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nome, cognome, password, sesso])

# Funzione per verificare se l'utente è già registrato nel file CSV
def utente_registrato(nome, cognome):
    try:
        with open(file_utenti, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nome and row[1] == cognome:
                    return True
        return False
    except FileNotFoundError:
        return False

# Funzione per verificare le credenziali di login dell'utente nel file CSV
def verifica_utente(username, cognome, password):
    try:
        with open(file_utenti, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == cognome and row[2] == password:
                    return True
        return False
    except FileNotFoundError:
        return False

@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/registrazione', methods=['GET', 'POST'])
def registra():
    if request.method == 'POST':
        nome = request.form.get('name')
        cognome = request.form.get('cognome')
        password = request.form.get('password')
        sesso = request.form.get('sesso')
        
        if utente_registrato(nome, cognome):
            return render_template('errore.html')
        else:
            if nome and cognome and password and sesso:
                salva_dati_utente(nome, cognome, password, sesso)
                return render_template('accesso_completato.html', nome=nome, cognome=cognome)
            else:
                return render_template('non_completata.html')

    return render_template('registrazione.html')

@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        cognome = request.form.get('cognome')
        password = request.form.get('password')
        
        if verifica_utente(username, cognome, password):
            return render_template('accesso_completato.html', nome=username, cognome=cognome)
        else:
            return render_template('errore.html')
    
    return render_template('login.html')

# Avvia l'app Flask
if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8085, debug=True)
