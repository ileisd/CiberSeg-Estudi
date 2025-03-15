#!/usr/bin/env python3

#Obliga a introduir un número sencer
n = int(input("Escriu un número entre l'1 i el 25: "))

#Valida que el número estigui entre l'1 i el 25
if not 1 <= n <= 25:
	print("Escriu un número vàlid.")

else:
	#Bucle per escriure tots els números entre n i 50 utilitzant un espai com a caracter final
	for i in range(n, 51):
		print(i, end=" ")
