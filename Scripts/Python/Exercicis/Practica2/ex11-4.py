#!/usr/bin/env python3

n = int(input("Introdueix un número del 10 al 20: "))

if 10 <= n <= 20:
	while n <= 50:
		#Si es parell, que sigui positiu
		if n % 2 == 0:
			print(n, end=",")
			n +=1
		else:
			#Converteix els senars en negatius
			print(-n, end=",")
			n +=1
else:
	print("ERROR. Número incorrecte.")
