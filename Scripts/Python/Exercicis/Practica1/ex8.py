#!/usr/bin/env python3

n = int(input("Introdueix un número entre el 5 i el 10: "))
#Variable que imprimeix els números de l'1 al 50.
r = 0
#Contador per saber quan imprimir r amb LF.
count = 1

#Validació de l'entrada de l'usuari
if 5 > n > 10:
	print("Introdueix un número vàlid.")
else:
	while r <= 50:
		#Imprimeix r, suma 1 al contador i comprova si el contador és n
		if count != n:
			print(r, end=" ")
			r +=1
			count +=1
		else:
			#Imprimeix r amb un salt de línea en comptes d'un espai
			print(r)
			r +=1
			count = 1

