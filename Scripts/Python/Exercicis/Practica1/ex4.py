#!/usr/bin/env python3
import random

#Obtenir el número aleatori per cada jugador amb el rang d'un D6
rng1 = random.randint(1,6)
rng2 = random.randint(1,6)

print(f"\nJUGADOR 1: {rng1}")
print(f"JUGADOR 2: {rng2}")

#Comparar els dos números dels daus
if rng1 > rng2:
	print("\nGuanya el jugador 1.")
elif rng1 < rng2:
	print("\nGuanya el jugador 2.")
else:
	print("Hi ha un empat.")
