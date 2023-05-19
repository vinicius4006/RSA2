import find_NZ.find_n_z as fnz

def mdc(n1: int, n2: int) -> int:
    """Calcula o mdc usando o algoritmo de Euclides"""
    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def co_primos(p: int, q: int, z: int) -> int:
    """Devolve uma lista com os coprimos"""
    b = 1
    coprimos = []
    while len(coprimos) < z:
        res = mdc(z, b)
        if res == 1:
            coprimos.append(b)
        b += 1    
            
    return coprimos

print(co_primos())