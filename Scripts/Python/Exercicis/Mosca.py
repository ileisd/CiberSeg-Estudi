#!/usr/bin/env python3
from random import randint

mosca = True
q = "[ ]"
qm = "[M]"
qx = "[X]"
qk = "[#]"

#Genera el tauler
print("MATA LA MOSCA: \n")
for x in range(1, 10):
        if x % 3 != 0:
            print(q, end= " ")
        else:
            print(q)

#Repeteix fins encertar el número
while mosca == True:
    n = int(input("Mata la mosca (1-9): "))
    print("\n")
    
    #Genera la posició de la mosca
    rng = randint(1, 9)
    
    #Imprimeix el tauler amb la mosca i el jugador
    for x in range(1, 10):
        if x % 3 != 0:
            #Posició del jugador
                #Posició de la mosca
            if x == rng:
                #Si el jugador encerta
                if rng == n:
                    print(qk, end= " ")
                    #Acaba el bucle
                    mosca = False
                #Si el jugador falla
                else:
                    print(qm, end= " ")
            elif x == n:
                print(qx, end= " ")
            else:
                print(q, end= " ")
        else:
            if x == rng:
                if rng == n:
                    print(qk)
                    mosca = False
                else:
                    print(qm)
            elif x == n:
                print(qx)
            else:
                print(q)

#final del joc
print("Finalment has matat la mosca.")

