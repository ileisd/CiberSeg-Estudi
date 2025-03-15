#!/usr/bin/env python3

n = int(input("Introdueix un número de l'1 al 50: "))

if 1 <= n <= 50:
	for x in range(1, 101):
		#Si el residu és 0 és divisible.
		if x % n == 0:
			print(x, end=",")
else:
	print("ERROR. Número incorrecte.")
