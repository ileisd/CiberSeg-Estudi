#!/usr/bin/env python3

#Introducció de les dos variables amb format de nombre sencer
n1 = int(input("Introdueix un número de l'1 al 25: "))
n2 = int(input("Introdueix un número entre l'2 i el 7: "))

#Validació de les dos variables introduides
if 1 > n1 > 25 or 2 > n2 > 7:
	print("Introdueix uns valors vàlids.")
else:
	for x in range(n1,101):
		#Fòrmula per imprimir N2 números i després saltar-se N2, ja que el contador no funciona per saltar N2 números amb for.
		if (x - n1) % (2 * n2) < n2:
			print(x, end=" ")
