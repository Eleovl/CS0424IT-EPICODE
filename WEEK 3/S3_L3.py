def calcola_perimetro_quadrato():
    lato = float(input("Inserisci la lunghezza del lato del quadrato: "))
    perimetro = 4 * lato
    return perimetro

def calcola_perimetro_triangolo():
    lato = float(input("Inserisci la lunghezza del lato del triangolo equilatero: "))
    perimetro = 3 * lato
    return perimetro

def calcola_perimetro_cerchio():
    raggio = float(input("Inserisci la lunghezza del raggio del cerchio: "))
    perimetro = 2 * 3.141592653589793 * raggio  # Usando il valore di pi greco
    return perimetro

def main():
    print("Scegli una figura geometrica:")
    print("1. Quadrato")
    print("2. Triangolo equilatero")
    print("3. Cerchio")
    
    scelta = input("Inserisci il numero della tua scelta: ")
    
    if scelta == '1':
        perimetro = calcola_perimetro_quadrato()
        figura = "quadrato"
    elif scelta == '2':
        perimetro = calcola_perimetro_triangolo()
        figura = "triangolo equilatero"
    elif scelta == '3':
        perimetro = calcola_perimetro_cerchio()
        figura = "cerchio"
    else:
        print("Scelta non valida.")
        return
    
    print(f"Il perimetro del {figura} è: {perimetro}")

# Eseguiamo la funzione principale
main()
