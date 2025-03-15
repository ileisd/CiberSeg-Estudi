#!/usr/bin/env python3

n = int(input("Escriu un número del 0 al 25: "))

if 0 <= n <= 25:
	for x in range(0, n + 1):
		if x == 0:
			#Imprimir el primer valor, que sempre serà 0
			if n != 0:
				print("0", end= ",")
			else:
				#En cas que n=0, imprimir només 0
				print("0")
		elif x < n:
			#Concatenació de strings i multiplicació de x cops la lletra que toqui
			print(str(x) + x*chr(65 + x), end= ",")
		else:
			print(str(x) + x*chr(65 + x))
else:
	print("ERROR.Número incorrecte.")
