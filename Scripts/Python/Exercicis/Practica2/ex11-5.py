#!/usr/bin/env python3

n = int(input("Escriu un número de l'1 al 5: "))

if 1 <= n <= 5:
	x = 1
	while x <= 20:
		if x % n != 0:
			print(x, end=",")
		else:
			print(x, end=",")
			i = 0
			#Imprimeix n asteriscs
			while i < n:
				print("*", end=",")
				i += 1
		x += 1
else:
    print("ERROR. Número incorrecte.")
