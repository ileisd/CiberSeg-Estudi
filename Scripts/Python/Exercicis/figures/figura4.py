#!/usr/bin/env python3

n = 0
while not 5 <= n <= 20:
    n = int(input("Introdueix un número entre el 5 i el 20: "))

for x in range(1, n + 1):
    if x == 1 or x == n:
        for _ in range(n):
            print("x", end= " ")
    else:
        for i in range(n, 0, -1):
            if i == 1 or i == x or i == n:
                print("x", end= " ")
            else:
                print(" ", end= " ")
    print()

