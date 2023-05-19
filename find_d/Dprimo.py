from random import sample
from math import isqrt

def mdc(n1: int, n2: int) -> int:
    """Calcula o mdc usando o algoritmo de Euclides"""
    while n2:
        n1, n2 = n2, n1 % n2
    return n1

def e_primo(num: int) -> bool:
    """Verifica se um número é primo"""
    if num < 2:
        return False
    for i in range(2, isqrt(num) + 1):
        if num % i == 0:
            return False
    return True

def co_primos(p: int, q: int, z: int) -> int:
    """Devolve um número primo aleatório entre 1 e z que seja coprimo com z"""
    b = 1
    coprimos = []
    while len(coprimos) < z:
        if mdc(b, z) == 1:
            coprimos.append(b)
        b += 1

    primos = [num for num in coprimos if e_primo(num)]
    d = sample(primos, 1)

    return int(d[0])
