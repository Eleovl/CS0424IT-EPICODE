import requests

def check_http_methods(target_url):
    methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'PATCH', 'CONNECT']
    supported_methods = []

    for method in methods:
        try:
            response = requests.request(method, target_url)
            # Se il server risponde, consideriamo il metodo supportato
            if response.status_code < 400:
                supported_methods.append(method)
        except requests.exceptions.RequestException as e:
            # Se c'è un'eccezione, potrebbe indicare che il metodo non è supportato
            pass

    return supported_methods

if __name__ == "__main__":
    target_ip = input("Inserisci l'IP del target (es. http://example.com): ")
    target_port = input("Inserisci la porta (es. 80 per HTTP, 443 per HTTPS): ")

    if not target_port.isdigit():
        print("Porta non valida, verrà utilizzata la porta predefinita.")
        target_url = target_ip
    else:
        # Costruisci l'URL con la porta specificata
        target_url = f"{target_ip}:{target_port}"

    supported_methods = check_http_methods(target_url)

    if supported_methods:
        print(f"Metodi HTTP supportati per {target_url}:")
        for method in supported_methods:
            print(f"- {method}")
    else:
        print(f"Nessun metodo HTTP supportato trovato per {target_url}.")