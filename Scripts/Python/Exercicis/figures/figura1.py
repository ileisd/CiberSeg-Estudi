#!/usr/bin/env python3

n = 0
while not 5 <= n <= 20:
    n = int(input("Introdueix un número entre el 5 i el 20: "))

for _ in range(n):
    for _ in range(n):
        print("x", end=" ")
    print()
