#!/usr/bin/env python3

n = int(input("Escriu un número del 0 al 25: "))

if 0 <= n <= 25:
	#Definir el rang a partir de 65(A)+n fins 91 (Z+1)
	for x in range (n + 65, 91):
		if x < 90:
			print(chr(x), end =",")
		else:
			print(chr(x))
else:
	print("ERROR. Número incorrecte.")
