#!/usr/bin/env python3

n = int(input("Introdueix un número de l'1 al 10: "))

if 1 <= n <= 10:
	for x in range(n, 21):
		if x < 20:
			print(x, end=",")
			print("*", end=",")
		else:
			print(x)
else:
	print("[ERROR] Número incorrecte.")
