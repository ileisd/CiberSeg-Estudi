#!/usr/bin/env python3

n = 0
a = " "

while not 65 <= ord(a) <= 90:
    a = input("Introdueix una lletra de la A la Z: ")
    a = a.upper()

while not 5 <= n <= 20:
    n = int(input("Introdueix un número entre el 5 i el 20: "))

for x in range(n):
    for i in range(n * 2):
        if i <= (n - x) or i >= (n + x):
            print(" ", end=" ")
        else:
            print(a, end= " ")
    print()

for y in range(n, 0, -1):
    for j in range(n * 2):
        if j <= (n - y) or j >= (n + y):
            print(" ", end=" ")
        else:
            print(a, end= " ")
    print()

