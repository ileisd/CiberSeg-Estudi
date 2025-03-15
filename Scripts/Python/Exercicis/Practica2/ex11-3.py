#!/usr/bin/env python3

n = int(input("Introdueix un número de l'1 al 50: "))
x = 1

if 1 <= n <= 50:
	while x <= 100:
		#Si el residu és 0 és divisible.
		if x % n == 0:
			print(x, end=",")
		x +=1
else:
	print("ERROR. Número incorrecte.")
