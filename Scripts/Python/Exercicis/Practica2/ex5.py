#!/usr/bin/env python3

n = int(input("Escriu un número de l'1 al 5: "))

if 1 <= n <= 5:
	for x in range(1,21):
		#Cada posició n, imprimeix n cops l'asterisc.
		if x % n != 0:
			print(x, end=",")
		else:
			print(x, end=",")
			for i in range (n):
				print("*", end=",")
else:
	print("ERROR. Número incorrecte.")
