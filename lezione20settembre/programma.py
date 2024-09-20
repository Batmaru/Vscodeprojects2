from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# File CSV per salvare le credenziali
csv_file = 'utenti_registrati.csv'
# File CSV per gli ordini
ordini_file = 'ordini.csv'

# Funzione per registrare un utente nel file CSV
def registra_utente_csv(nome, cognome, username, password):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Nome', 'Cognome', 'Username', 'Password'])
        writer.writerow([nome, cognome, username, password])

# Funzione per verificare se l'utente è registrato
def utente_registrato(username, password=None):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    if password is None or row['Password'] == password:
                        return row['Nome'], row['Cognome']
        return None
    except FileNotFoundError:
        return None

# Funzione per registrare l'ordine
def registra_ordine_csv(username, ordine):
    file_exists = os.path.isfile(ordini_file)
    with open(ordini_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Username', 'Ordine'])
        writer.writerow([username, ordine])

# Funzione per recuperare tutti gli ordini di un utente
def recupera_ordini(username):
    ordini = []
    try:
        with open(ordini_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    ordini.append(row['Ordine'])
    except FileNotFoundError:
        pass
    return ordini

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = utente_registrato(username, password)
        if user:
            nome, cognome = user
            return redirect(url_for('pagina_personale', nome=nome, cognome=cognome, username=username))
        else:
            flash('Credenziali errate o utente non registrato.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'POST':
        nome = request.form['name']
        cognome = request.form['cognome']
        username = request.form['username']
        password = request.form['password']
        conferma_password = request.form['conferma_password']
        
        if password != conferma_password:
            flash('Le password non coincidono.')
            return redirect(url_for('registrazione'))
        
        # Controllo se lo username esiste già
        if utente_registrato(username):
            flash('Username già in uso. Scegli un altro username.')
            return redirect(url_for('registrazione'))
        
        # Registra l'utente
        registra_utente_csv(nome, cognome, username, password)
        flash('Registrazione completata con successo!')
        return redirect(url_for('login'))
    
    return render_template('registrazione.html')

@app.route('/pagina_personale/<nome>/<cognome>/<username>')
def pagina_personale(nome, cognome, username):
    ordini = recupera_ordini(username)
    return render_template('pagina_personale.html', nome=nome, cognome=cognome, username=username, ordini=ordini)

@app.route('/effettua_ordine/<username>', methods=['GET', 'POST'])
def effettua_ordine(username):
    if request.method == 'POST':
        # Gestione dell'ordine
        nuovo_ordine = request.form.get('ordine')
        registra_ordine_csv(username, nuovo_ordine)  # Aggiunge il nome utente e l'ordine
        return redirect(url_for('ordini_vecchi', username=username))  # Reindirizza alla pagina ordini vecchi
    return render_template('effettua_ordine.html', username=username)


@app.route('/ordini_vecchi/<username>')
def ordini_vecchi(username):
    ordini = recupera_ordini(username)
    return render_template('ordini_vecchi.html', ordini=ordini, username=username)


if __name__ == '__main__':
    app.run(debug=True)
