#!/usr/bin/env python3

n = int(input("Introdueix un número de l'1 al 25: "))
x = 0

if 1 <= n <= 25:
	while x <= 50:
		if x < 50:
			# El residu tindrà un valor entre 0 i n-1, pel que imprimirà les lletres dintre el rang n que li donem.
			print(chr(65 + (x % n)), end=",")
			x +=1
		else:
			print(chr(65 + (x % n)))
			x +=1
else:
	print("ERROR. Número incorrecte.")

