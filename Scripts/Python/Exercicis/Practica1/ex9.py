#!/usr/bin/env python3

n = int(input("Introdueix un número entre el 10 i el 20: "))
x = 1

if 20 < n or n < 10:
	print("Introdueix un número vàlid.")
else:
	while n >= x:
		print(x**2, end=" ")
		x +=1
