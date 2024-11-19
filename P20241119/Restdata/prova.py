from P20241119.Restdata.dbclient import connect, close

cur = connect()
if cur:
    print("Connessione al database riuscita!")
    close(cur)
else:
    print("Errore nella connessione al database.")
