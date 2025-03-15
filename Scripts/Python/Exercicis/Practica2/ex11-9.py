#!/usr/bin/env python3

l = input("Introdueix una lletra de la A la Z: ")
#Transforma l'input en majúscula i al seu número corresponent per poder fer la comprovació
l_up = l.upper()
l_num = ord(l_up)
x = 1

if 65 <= l_num <= 90:
	while x <= 5:
		lletra = l_num + x
		if x < 5:
			if lletra > 90:
				print(chr(lletra - 26), end= ",")
				x +=1
			else:
				print(chr(lletra), end= ",")
				x +=1
		else:
			if lletra > 90:
				print(chr(lletra - 26), end= " ")
				x +=1
			else:
				print(chr(lletra), end= " ")
				x +=1

	print(f"- ({l_up}) -", end= " ")

	while x >= 0:
		lletra = l_num + x
		if x > 1:
			if lletra > 90:
				print(chr(lletra - 26), end= ",")
				x -=1
			else:
				print(chr(lletra), end= ",")
				x -=1
		else:
			if lletra > 90:
				print(chr(lletra - 26))
				x -=1
			else:
				print(chr(lletra))
				x -=1
else:
	print("Error")
