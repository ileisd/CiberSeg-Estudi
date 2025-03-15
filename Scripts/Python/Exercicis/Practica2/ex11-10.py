#!/usr/bin/env python3

n = int(input("Escriu un número del 0 al 25: "))
x = 0

if 0 <= n <= 25:
	while x <= n:
		if x == 0:
			#Imprimir el primer valor, que sempre serà 0
			if n != 0:
				print("0", end= ",")
				x +=1
			else:
				#En cas que n=0, imprimir només 0
				print("0")
		elif x < n:
			#Concatenació de strings i multiplicació de x cops la lletra que toqui
			print(str(x) + x*chr(65 + x), end= ",")
			x +=1
		else:
			print(str(x) + x*chr(65 + x))
			x +=1
else:
	print("ERROR.Número incorrecte.")
