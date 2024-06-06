#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Funzione per presentare il menu iniziale
void mostraMenu() {
    printf("Benvenuto allo squid game!\n");
    printf("Scegli una delle seguenti opzioni:\n");
    printf("A) Inizia una nuova partita\n");
    printf("B) Esci dal gioco\n");
}

// Funzione per gestire una nuova partita
void nuovaPartita() {
    char nome[50];
    int punteggio = 0;

    printf("Inserisci il tuo nome: ");
    scanf("%s", nome);

    // Esempio di domande e risposte
    char risposte[][50] = {
        "Qual è la prima prova?",
        "A) Tiro alla fune\nB) Un,due,tre stella\nC) biglie\n",
         "B",
        "Quale forma è la più difficile da staccare?",
        "A) Triangolo\nB) Cerchio\nC) Stella\n",
         "C",
        "Quante persone vicono lo Squid Game?",
        "A) 1\nB) 2\nC) nessuno\n",
         "A"
        
    };

    // Calcola il punteggio
    for (int i = 0; i < sizeof(risposte) / sizeof(risposte[0]); i += 3) {
        printf("%s\n%s", risposte[i], risposte[i + 1]);
        char rispostaUtente;
        scanf(" %c", &rispostaUtente);
        if (rispostaUtente == risposte[i + 2][0]) {
            punteggio++;
        }
    }

    printf("\n%s, hai totalizzato %d punti!\n", nome, punteggio);
}

int main() {
    char scelta;

    do {
        mostraMenu();
        scanf(" %c", &scelta);

        switch (scelta) {
            case 'A':
                nuovaPartita();
                break;
            case 'B':
                printf("Arrivederci!\n");
                exit(0);
            default:
                printf("Scelta non valida. Riprova.\n");
        }
    } while (1);

    return 0;
}
