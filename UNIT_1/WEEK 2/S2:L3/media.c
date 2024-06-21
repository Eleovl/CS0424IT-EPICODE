#include <stdio.h>

int main () {
    int pollo, tacchino; 
    float media;

    //Richiesta di inserire il primo animale
    printf("inserisci quanti polli ci sono:");
    scanf("%d",&pollo);

    //Richiesta di inserire il secondo animale
    printf("inserisci quanti tacchini ci sono:");
    scanf("%d",&tacchino);

    //Calcolo della media 
    media = (pollo + tacchino) / 2.0;

    //Risultato

    printf("nella fattoria ci sono pollo (%d) e tacchino (%d) %.2f\n", pollo, tacchino, media);

}