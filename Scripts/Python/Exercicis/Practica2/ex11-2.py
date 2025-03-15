#!/usr/bin/env python3

n = int(input("Introdueix un número de l'1 al 10: "))

if 1 <= n <= 10:
	while n <= 20:
		if n < 20:
			print(n, end=",")
			print("*", end=",")
			n +=1
		else:
			print(n)
			n +=1
else:
	print("[ERROR] Número incorrecte.")
