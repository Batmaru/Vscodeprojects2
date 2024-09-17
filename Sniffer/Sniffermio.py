import csv
import time
from scapy.all import *  # Importa tutte le funzioni di Scapy, utile per lo sniffing di pacchetti
from scapy.layers.inet import IP, TCP  # Importa i protocolli IP e TCP, necessari per identificare i pacchetti di rete
from scapy.layers.http import HTTPRequest  # Importa il livello HTTP, per riconoscere le richieste HTTP

# Nome del file CSV dove salveremo i dati delle connessioni
output_file = "web_connections.csv"

# Inizializzare il file CSV e scrivere l'intestazione delle colonne
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["data-ora", "ip_src", "ip_dst", "tcp_src", "tcp_dst", "host"])

# Funzione che processa ogni pacchetto catturato
def process_pkt(pkt):
    if IP in pkt and TCP in pkt:  # Controlla se il pacchetto contiene protocolli IP e TCP
        ip_src = pkt[IP].src  # Estrai l'indirizzo IP sorgente
        ip_dst = pkt[IP].dst  # Estrai l'indirizzo IP di destinazione
        tcp_src = pkt[TCP].sport  # Estrai la porta sorgente TCP
        tcp_dst = pkt[TCP].dport  # Estrai la porta di destinazione TCP
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Ottieni il timestamp corrente

        # Verifica se è una richiesta HTTP e estrai l'host, altrimenti consideralo HTTPS
        if pkt.haslayer(HTTPRequest):  
            host = pkt[HTTPRequest].Host or ""  # Estrai il nome dell'host (se presente)
        else:
            host = "HTTPS"  # Se non è HTTP, trattalo come HTTPS (senza dettagli)

        # Scrivi le informazioni nel file CSV
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, ip_src, ip_dst, tcp_src, tcp_dst, host])

# Avvia lo sniffing dei pacchetti su porte HTTP (80) e HTTPS (443)
sniff(iface="eth0", filter="tcp port 80 or tcp port 443", prn=process_pkt)
