#!/usr/bin/env python3

n = 0
while not 5 <= n <= 20:
    n = int(input("Introdueix un número entre el 5 i el 20: "))

for x in range(n + 1):
    for i in range(n + 1):
        if i == x or i == 0 or x == n:
            print("x", end= " ")
        else:
            print(" ", end= " ")
    print()
