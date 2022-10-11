#include <stdio.h>
#include <stdlib.h>

char wordgenerator(int zahl){
    char* word = "";
    for (int i = 0; i < zahl; i++){
        word += itoa(rand()%2);
    }
    return word;
}

char encoder(char* word){
    char* encoded = "";
    for (int i = 0; i < sizeof word/sizeof *word; i++){
        encoded += 3*word[i];
    }
}

int main(int argc, char **argv) {
    printf(encoder("010"));
    return 0;
}
