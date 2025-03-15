#!/usr/bin/env python3

#Introducció de les dos variables amb format de nombre sencer
n1 = int(input("Introdueix un número de l'1 al 25: "))
n2 = int(input("Introdueix un número entre l'2 i el 7: "))

#Validació de les dos variables introduides
if 1 > n1 > 25 or 2 > n2 > 7:
	print("Introdueix uns valors vàlids.")
else:
	#Variable per contar quan s'ha de fer el salt de números
	count = 0
	while n1 <= 100:
		#Quan el contador arriba a n2, salta n2 números i es reinicia
		if count != n2:
			print(n1, end=" ")
			n1 +=1
			count += 1
		else:
			n1 +=n2
			count = 0
