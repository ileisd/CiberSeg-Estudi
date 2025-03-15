#!/usr/bin/env python3

n = int(input("Número: "))
b = int(input("Base (entre 2 i 16): "))

if 2 <= b <= 16:
    nf = n
    canvi = []

    while n >= b:
        canvi.append(str(n % b))
        n = n // b

    canvi.append(str(n))

    canvi = ''.join(reversed(canvi))

    print(f"\n{nf} b10 = {canvi} b{b}")
else:
    print("Introdueix una base entre 2 i 16.")
