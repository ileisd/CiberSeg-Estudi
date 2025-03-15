#!/usr/bin/env python3

#Introducció de la variable
preu = float(input("Introdueix un preu entre 10 i 1000 (pot tenir decimals): "))
#Arrodoniment a dos decimals per fer càlculs més propers al sistema monetari
round(preu, 2)

#Definir els tres rangs de números i els seus càlculs
if preu <= 100:
	preu*=1.21
elif preu <= 500:
	preu*=1.18
	preu*=0.95
else:
	preu*=1.15
	preu*=0.90

print(f"El preu final és de {preu_final}€")
