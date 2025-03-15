#!/usr/bin/env python3

n = int(input("Introdueix un número del 0 al 25: "))
x = 90

if 0 <= n <= 25:
	while x >= (65 + n):
		if x > (65 + n):
			print(chr(x), end=",")
			x -=1
		else:
			print(chr(x))
			x -=1
else:
	print("ERROR. Número incorrecte")

