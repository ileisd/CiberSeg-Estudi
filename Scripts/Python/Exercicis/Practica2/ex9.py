#!/usr/bin/env python3

l = input("Introdueix una lletra de la A la Z: ")
#Transforma l'input en majúscula i al seu número corresponent per poder fer la comprovació
l_up = l.upper()
l_num = ord(l_up)

if 65 <= l_num <= 90:
	for x in range(1, 6):
		lletra = l_num + x
		if x < 5:
			if lletra > 90:
				print(chr(lletra - 26), end= ",")
			else:
				print(chr(lletra), end= ",")
		else:
			if lletra > 90:
				print(chr(lletra - 26), end= " ")
			else:
				print(chr(lletra), end= " ")

	print(f"- ({l_up}) -", end= " ")

	for x in range(5, 0, -1):
		lletra = l_num + x
		if x > 1:
			if lletra > 90:
				print(chr(lletra - 26), end= ",")
			else:
				print(chr(lletra), end= ",")
		else:
			if lletra > 90:
				print(chr(lletra - 26))
			else:
				print(chr(lletra))
else:
	print("Error")

