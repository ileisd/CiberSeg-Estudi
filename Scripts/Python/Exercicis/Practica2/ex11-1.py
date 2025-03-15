#!/usr/bin/env python3

n = int(input("Introdueix un número del 10 al 20: "))
v = int(input("Escull positiu (1) o negatiu (0): "))
count = 0

#Comprovació del rang del primer número
if 10 <= n <= 20:
	#Valor positiu
	if v == 1:
		while n <= 50:
			#Imprimir només count amb un LF, en cas de l'últim número
			if n < 50:
				print(n, end=",")
				n +=1
			else:
				print(n)
				n +=1
	#Valor negatiu
	elif v == 0:
		while n >= -30:
			if n > -30:
				print(n, end=",")
				n -=1
			else:
				print(n)
				n -=1
	#Error de valor
	else:
		print("ERROR. Valor incorrecte.")
else:
	print("ERROR. Número incorrecte.")
