#include <stdio.h>

int main () {

    int cane, gatto, prodotto;

    //richiesta all'utente di inserire il primo numero
    printf("inserisci il primo animale");
    scanf ("%d", &cane);

    //richiesta all'utente di inserire il secondo numero
    printf("inserisci il secondo animale");
    scanf ("%d", &gatto);

    //moltiplicazione
    prodotto = cane * gatto;
    //risultato
    printf("lo zoo risulta pieno %d e %d è: %d\n",cane, gatto, prodotto);

    return 0;
}
