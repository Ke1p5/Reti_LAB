#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progetto Programmazione di Reti - Traccia 2: Web Server Semplice

@author: Federico Capponi - federico.capponi@studio.unibo.it
# Matricola = 0001059826
"""

import socket
import sys

def request_connection(host, port, file_id):
    # Inizializza il socket del patreon
    patreon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Costruisce la richiesta GET
    plea = "GET /" + file_id + " HTTP/1.1 \r\n\r\n"
        
    try: 
        # Si connette al server
        patreon.connect((host, port))
    except Exception as error:
        print (Exception,":",error)
        print ("Could not establish connection.\r\n")
        sys.exit(0)

    # Invia la richiesta al server
    patreon.send(plea.encode())

    # Salva la risposta del server
    ext = str(file_id).rsplit('.', 1)[-1].replace('\'', '')
    # Riceve  in formato binario in modo da visualizzare immagini su browser
    if (ext == 'png' or ext == 'jpeg' or ext == 'jpg' or ext == 'gif') :
        answer = patreon.recv(1024)
    # Altrimenti fa il decoding del testo
    else :
        answer = patreon.recv(1024).decode()

    # Stampa la risposta
    print("Server's response':\n", answer)

    # Chiude il socket del patreon
    patreon.close()

if __name__ == "__main__":
    print("Please insert server's IP address (default localhost): ")
    HOST = input().strip() or 'localhost' # Indirizzo IP del server
    print("Now input port's number (default 8080): ")
    PORT = int(input().strip() or 8080) # Porta su cui il server resta in ascolto
    print("Finally specify the file's name to obtain through the GET request (default index.html): ")
    FILE_ID = input().strip() or 'index.html' # File che viene richiesto al server

    # Inizializza la richiesta
    request_connection(HOST, PORT, FILE_ID)
