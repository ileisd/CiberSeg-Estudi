#!/usr/bin/env python3

n = int(input("Introdueix un número del 10 al 20: "))

if 10 <= n <= 20:
	for x in range(n,51):
		#Si es parell, que sigui positiu
		if x % 2 == 0:
			print(x, end=",")
		else:
			#Converteix els senars en negatius
			x -= 2*x
			print(x, end=",")
else:
	print("ERROR. Número incorrecte.")
