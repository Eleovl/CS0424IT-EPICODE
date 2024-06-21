import socket
import argparse
import threading
from queue import Queue
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Funzione per effettuare il lookup dei servizi delle porte comuni
def get_service(port):
    try:
        service = socket.getservbyport(port)
        if service == "domain":
            return "DNS"
        return service
    except socket.error:
        return "Servizio sconosciuto"

# Funzione di scansione della porta
def scan_port(ip, port, output, thread_id):
    try:
        logging.info(f"Thread {thread_id} - Invio pacchetto di dati alla Porta: {port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = get_service(port)
            output.put((port, service, "Aperta"))
        else:
            output.put((port, "Servizio sconosciuto", "Chiuso"))
    except socket.timeout:
        logging.warning(f"Thread {thread_id} - Timeout scansione Porta: {port}")
        output.put((port, "Servizio sconosciuto", "Chiuso"))
    except socket.error as e:
        logging.error(f"Thread {thread_id} - Errore Socket, scansione Porta: {port}: {e}")
        output.put((port, "Servizio sconosciuto", "Chiuso"))
    except Exception as e:
        logging.error(f"Thread {thread_id} - Errore inatteso, scansione Porta: {port}: {e}")
        output.put((port, "Servizio sconosciuto", "Chiuso"))

# Funzione per il worker del thread
def worker(ip, port_queue, output, thread_id):
    while not port_queue.empty():
        port = port_queue.get()
        print(f"Numero del Thread inviato: {thread_id} alla Porta: {port}")
        try:
            scan_port(ip, port, output, thread_id)
        finally:
            port_queue.task_done()

# Funzione per scansionare le porte in parallelo utilizzando multithreading
def scan_ports(ip, start_port, end_port, num_threads):
    port_queue = Queue()
    output = Queue()

    # Riempire la coda con il range di porte
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Creare e avviare i thread
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip, port_queue, output, i+1))
        thread.start()
        threads.append(thread)

    # Aspettare che tutti i thread abbiano terminato
    for thread in threads:
        thread.join()

    # Raccogliere i risultati
    results = []
    while not output.empty():
        results.append(output.get())

    return results

# Funzione principale
def main():
    try:
        # Richiesta dati all'utente
        target_ip = input("Inserisci l'IP target: ")
        start_port = int(input("Inserisci la porta di inizio: "))
        end_port = int(input("Inserisci la porta di fine: "))
        num_threads = int(input("Inserisci il numero di thread: "))

        # Verifica validità indirizzo IP
        try:
            socket.inet_aton(target_ip)
        except socket.error:
            logging.error("Invalid IP address format.")
            return

        results = scan_ports(target_ip, start_port, end_port, num_threads)

        if results:
            print("Risultati della scansione:")
            for port, service, status in sorted(results):
                print(f"Porta: {port} Servizio: {service} Stato: ({status})")
        else:
            print("No ports found.")
    except ValueError:
        print("Inserimento non valido, riprovare.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
    main()