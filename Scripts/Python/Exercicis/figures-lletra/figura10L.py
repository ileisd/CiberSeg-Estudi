#!/usr/bin/env python3

n = 0
a = " "

while not 65 <= ord(a) <= 90:
    a = input("Introdueix una lletra de la A la Z: ")
    a = a.upper()

while not 5 <= n <= 20:
    n = int(input("Introdueix un número entre el 5 i el 20: "))

for x in range(n):
    for i in range(1, n * 2):
        if i == (n - x) or i == (n + x) or n - 1 == x:
            print(a, end=" ")
        else:
            print(" ", end= " ")
    print()

