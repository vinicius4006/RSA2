from random import sample

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
        print(b, '--',res)
        if res == 1:
            coprimos.append(res)
        b += 1
        
            
    
    d = sample(coprimos, 1)
    return int(d[-1])