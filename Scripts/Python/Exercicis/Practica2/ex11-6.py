#!/usr/bin/env python3

n = int(input("Escriu un número del 0 al 25: "))
#Variable per començar l'abecedari des del punt n
x = 65 + n

if 0 <= n <= 25:
	while 65 <= x <= 90:
		if x < 90:
			print(chr(x), end =",")
			x +=1
		else:
			print(chr(x))
			x +=1
else:
	print("ERROR. Número incorrecte.")
