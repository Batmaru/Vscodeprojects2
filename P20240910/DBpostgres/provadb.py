import sys
import os
import os.path
import time

#pip3 install psycopg2-binary
import dbclient as db


print("Inizio programma prova database")
cur = db.connect()
if cur is None:
	print("Errore connessione al DB")
	sys.exit()

sQuery = "insert into cittadini (codice_fiscale, nome, cognome, data_di_nascita) VALUES ('224133', 'maru', 'raf', '2004-07-02');"
# db.write_in_db(cur,sQuery)


sQuery = "select * from Cittadini;"
iNumRows = db.read_in_db(cur,sQuery)
for ii in range(0,iNumRows):
	myrow = db.read_next_row(cur)
	print(myrow)
	