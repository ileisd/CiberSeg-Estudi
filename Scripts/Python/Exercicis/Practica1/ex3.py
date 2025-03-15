#!/usr/bin/env python3
import random

#Definir el rang del número aleatori i convertir-lo en str per poder separar-lo per caràcters.
rng = str(random.randint(100,999))

#Separar cada caràcter i comparar-lo
if (rng[1] == rng[2]) and (rng[2] == rng[3]):
	print(f"El número {rng} és cap-i-cua.")
else:
	print(f"El número {rng} no és cap-i-cua.")
