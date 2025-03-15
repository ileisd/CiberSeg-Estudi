#!/usr/bin/env python3

n = int(input("Introdueix un número del 10 al 20: "))
v = int(input("Escull positiu (1) o negatiu (0): "))

#Comprovació del rang del primer número
if 10 <= n <= 20:
	#Valor positiu
	if v == 1:
		for x in range(n, 51):
			#Imprimir només x amb un LF, en cas de l'últim número
			if x < 50:
				print(x, end=",")
			else:
				print(x)
	#Valor negatiu
	elif v == 0:
		for x in range(n, -31, -1):
			if x > -30:
				print(x, end=",")
			else:
				print(x)
	#Error de valor
	else:
		print("ERROR. Valor incorrecte.")
else:
	print("ERROR. Número incorrecte.")
