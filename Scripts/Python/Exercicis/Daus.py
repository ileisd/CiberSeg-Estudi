#!/usr/bin/env python3
from random import randint

j1 = 0
j2 = 0

#Repeteix el codi 7 cops per simular 7 tirades
for _ in range(7):
    empat = 1
    #Repeteix tirada en cas d'empat (empat = 1)
    while empat > 0:
        #Tirada del J1
        rnum11 = randint(1, 6)
        rnum12 = randint(1, 6)

        #Tirada del J2
        rnum21 = randint(1, 6)
        rnum22 = randint(1, 6)

        print(f"JUGADOR 1: {rnum11} {rnum12}")
        print(f"JUGADOR 2: {rnum21} {rnum22}")

        #Dobles
        if rnum11 == rnum12 or rnum21 == rnum22:
        #Dobles pel J1
            if rnum11 == rnum12:
                print(f"\nGuanya el JUGADOR 1 per doble {rnum11}.\n")
                j1 +=1
                empat = 0
            #Dobles pel J2
            elif rnum22 == rnum21:
                print(f"\nGuanya el JUGADOR 2 per doble {rnum21}.\n")
                j2 +=1
                empat = 0
            #Dobles pels 2 jugadors
            elif rnum11 == rnum12 and rnum21 == rnum22:
                #El J1 té el número més gran
                if rnum11 > rnum21:
                    print(f"\nGuanya el JUGADOR 1 per doble {rnum11}.\n")
                    j1 +=1
                    empat = 0
                #El J2 té el número més gran
                elif rnum11 < rnum21:
                    print(f"\nGuanya el JUGADOR 2 per doble {rnum21}.\n")
                    j2 +=1
                    empat = 0
                #Els 2 números són iguals i torna a tirar.
                else:
                    print("\nEmpat a doble {rnum11}.\n")

        #Suma de números diferents
        else:
            r1 = rnum11 + rnum12
            r2 = rnum21 + rnum22
        
            if r1 > r2:
                print(f"\nGuanya el JUGADOR 1 amb una suma de {r1}.\n")
                empat = 0
                j1 +=1
            elif r1 < r2:
                print(f"\nGuanya el JUGADOR 2 amb una suma de {r2}.\n")
                j2 +=1
                empat = 0
            else:
                print("\nEmpat.\n")

#Imprimeix el resultat final separat d'una línia
print("--------------------------------------------")
num21 = randint(1, 6)
if j1 > j2:
    print(f"\nGuanya el JUGADOR 1: [ {j1} ] - [ {j2} ]")
else:
    print(f"\nGuanya el JUGADOR 2: [ {j2} ] - [ {j1} ]")
