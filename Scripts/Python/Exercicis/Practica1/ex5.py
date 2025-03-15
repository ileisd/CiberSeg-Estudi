#!/usr/bin/env python3
import random

#Variable per contar els empats que hi ha hagut
empat = 1

#Bucle per fer una nova tirada en cas d'empat
while 0 < empat <= 2:
	#Genera un número de l'1 al 6, simulant un D6
	rng1 = random.randint(1,6)
	rng2 = random.randint(1,6)

	print(f"\nJUGADOR 1: {rng1}")
	print(f"JUGADOR 2: {rng2}")

	if rng1 > rng2:
		print("\nGuanya el jugador 1.")
		#La variable "empat" a 0 indica una sortida del programa
		empat = 0
	elif rng1 < rng2:
		print("\nGuanya el jugador 2.")
		empat = 0
	else:
		#Primera tirada de desempat 
		if empat < 2:
			print("\nHi ha un empat.")
			input("Apreta qualsevol tecla per fer la tirada de desempat.")
			#Sumant 1 a la variable s'indica que el 2n desempat sigui a cara o creu
			empat +=1
		else:
			#Cara o creu
			print("\nHi ha un altre empat.")
			input("Apreta qualsevol tecla per jugar a cara o creu.")
			#La variable moneda escull entre 1 i 2, simulant les cares d'una moneda
			moneda = random.randint(1,2)
			if moneda == 1:
				print("\nCara: guanya el JUGADOR 1.")
				empat = 0
			else:
				print("\nCreu: guanya el JUGADOR 2.")
				empat = 0
