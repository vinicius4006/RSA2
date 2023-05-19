from random import sample

def mdc(n1: int, n2: int) -> int:
    """Calcula o mdc usando o algoritmo de Euclides"""
    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def co_primos(p: int, q: int, z: int) -> int:
    """Devolve um número primo aleatório entre 1 e z que seja coprimo com z"""
    b = 1
    coprimos = []
    while len(coprimos) < z:
        res = mdc(z, b)
        if res == 1:
            coprimos.append(b)
        b += 1
        
    d = sample(coprimos, 1)
    return int(d[0])