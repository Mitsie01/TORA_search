#include <stdio.h>

float dt;
float t;
unsigned int Z;
float gamma;


int main(){

    dt = 0.01;
    Z = 25;
    gamma = 0.5;


    for(t = 0; t <= Z; t = t+dt){

        printf("%.2f\n", t);
    }

    return 0;
}