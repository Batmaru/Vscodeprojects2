import csv
import time
from scapy.all import * 
from scapy.layers.inet import IP, TCP  
from scapy.layers.http import HTTPRequest, HTTPResponse

output_file = "web_connections.csv"


with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["data-ora", "ip_src", "ip_dst", "tcp_src", "tcp_dst", "host"])

def process_pkt(pkt):
    if IP in pkt and TCP in pkt:  
        ip_src = pkt[IP].src  
        ip_dst = pkt[IP].dst  
        tcp_src = pkt[TCP].sport 
        tcp_dst = pkt[TCP].dport  
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  
        #timestamp = time.ctime()


        if tcp_dst == 80 and pkt.haslayer(HTTPRequest):
            host = pkt[HTTPRequest].Host.decode() if pkt[HTTPRequest].Host else ""  

        elif tcp_src == 80 and pkt.haslayer(HTTPResponse):
            host =pkt[HTTPResponse].Server.decode() if pkt[HTTPResponse].Server else ""  
        #     host="DA VEDERE"
        #     print(pkt[HTTPResponse].show())
        else:
            host = "HTTPS"  


        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, ip_src, ip_dst, tcp_src, tcp_dst, host])

sniff(iface="eth0", filter="tcp port 80 or tcp port 443", prn=process_pkt)
