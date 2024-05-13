#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Progetto Programmazione di Reti - Traccia 2: Web Server Semplice

@author: Federico Capponi - federico.capponi@studio.unibo.it
# Matricola = 0001059826
"""

import socket
import threading

def patreon_dealing(served):
    
    try :
        msg = served.recv(1024)
    
        if len(msg.split())>0:
            file_path = msg.split()[1]
            print (msg, '::', msg.split()[0],':', file_path)
            file_id = file_path[1:]
            print (file_path, '||', file_id)
            ext = str(file_id).rsplit('.', 1)[-1].replace('\'', '')
            print(ext)
            # Apre il file in formato binario in modo da visualizzare immagini su browser
            if (ext == 'png' or ext == 'jpeg' or ext == 'jpg' or ext == 'gif') :
                f = open(file_id, 'rb')
                page = f.read()
                served.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                served.send(page)
            # Altrimenti apre in modalità testuale
            else :
                f = open(file_id, 'r+')
                page = f.read().encode()
                served.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                served.send(page)
                served.send("\r\n".encode())

            print(page)
            # Invia la risposta al patreon
            
    except IOError :
        # Casistica per un file richiesto non esistente
        answer = "HTTP/1.1 404 Not found\r\n\r\nERROR 404: Not Found. The file you're looking for isn't here!"
        served.send(answer.encode())

    except socket.error as exc:
         # Casistica per un eventuale errore di connessione del socket lato server
         answer = "HTTP/1.1 500 Server error\r\n\r\nOops, something went wrong, and the server could not handle that request!r\n\r\n" + exc
         served.send(answer.encode())

    finally :
        # Chiude la connessione
        served.close()

def server_init(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)  # Accetta una sola connessione pendente, può essere modificato a piacere (facendo attenzione)

    # Inizializzazione del vettore per i Thread
    thread_vector = []
    print("Server listening at address: ", host, " on port: ", port)
    
    try :        
        while True : 
            print("Ready to accept connections...")
            served, patreon_id = server.accept()
            print("Link accepted from: ", patreon_id[0], " on port: ", patreon_id[1])
            print(served, patreon_id)
    
            # Avvia un nuovo thread per gestire la richiesta
            patreon_manage = threading.Thread(target=patreon_dealing, args=(served, ))
            patreon_manage.daemon = True
            patreon_manage.start()
            # Aggiungo il Thread al vettore
            thread_vector.append(patreon_manage)
    
    except KeyboardInterrupt:
        # Per SIGKILL 
        print('Forced server''s shutdown (Ctrl+C pressed)')
    
    finally :
        if server :
            server.close()
        for thread in thread_vector :
            thread.join()

if __name__ == "__main__":
    # Raccoglie input necessari da CLI
    print("Please insert server's IP address (default localhost): ")
    HOST = input().strip() or 'localhost' # Indirizzo IP del server
    print("Now input port's number (default 8080): ")
    PORT = int(input().strip() or 8080) # Porta su cui il server resta in ascolto
    
    # Inizializza il server
    server_init(HOST, PORT)
