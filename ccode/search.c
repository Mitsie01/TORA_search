#include <stdio.h>
#include <math.h>

double dt;
unsigned int t;
unsigned int Z;
double gamma;
double p1;
double p;


int main(){

    dt = 0.01;
    Z = 1;
    gamma = 0.4;
    p1 = 10;


    for(t = 0; t <= (Z/dt); t +=1){

        p = (1-pow((1-gamma), t))/(100/p1);
        printf("%.16lf - %u\n", p, t);
    }

    return 0;
}