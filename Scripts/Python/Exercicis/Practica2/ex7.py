#!/usr/bin/env python3

n = int(input("Introdueix un número del 0 al 25: "))

if 0 <= n <= 25:
	#En aquest cas, en comptes de sumar 1 al número final del rang se li resta perquè el step és -1.
	for x in range(90, (64 + n), -1):
		if x > (65 + n):
			print(chr(x), end=",")
		else:
			print(chr(x))
else:
	print("ERROR. Número incorrecte")

