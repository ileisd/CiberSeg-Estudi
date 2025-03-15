#!/usr/bin/env python3
import math

#Variable introduïda per l'usuari, de tipus float per poder introduir decimals
r = float(input("Introdueix un número del 2 al 10 (pot incloure decimals): "))

#Comprovació del rang del número
if 2 <= r <= 10:
	#Fòrmula del perímetre
	p = 2*math.pi*r
	#Fòrmula de l'àrea
	a = math.pi*r**2

	print(f"\nPerímetre = {p}")
	print(f"Àrea = {a}")
else:
	print("\nEl número no és correcte.")
