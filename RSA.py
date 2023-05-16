from random import sample


def creates_pnumbers(size: int) -> list[int]:
    """Cria números primos e armazena em uma lista"""
        
    primos = []
    for num in range(2, size+1):
        for i in range(2, num):
            if num % i == 0:
                break
            else:
                primos.append(num)
    return primos                


def product(numbers: list) -> tuple[int]:
    """Seleciona dois números aleatórios a partir da lista no parâmetro"""
                
    p, q = sample(numbers, 2)
    
    return p, q, p*q


def mdc(n1: int, n2: int) -> int:
    """Calcula o mdc usando o algoritmos de Euclides"""
    
    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def totiente(p: int, q: int, n: int) -> int:
    """Função de Totiente de Euler, calcula o número de coprimos
    a um determinado número, no nosso n = p*q."""
    
    return (p - 1) * (q - 1)
        

def co_primos(p: int, q: int, n: int, tot: int) -> list[int]:
    """Devolve uma lista com os coprimos"""

    b = 1
    coprimos = []
    while len(coprimos) < tot:
        
        res = mdc(n, b)
        if res == 1:
            coprimos.append(b)
        b += 1    
            
    return coprimos
            
def private_key(e: int, tot: int) -> int:
    """Retorna a chave D, a partir da seguinte fórmula e * d % tot == 1."""
    
    d = 1
    while True:
       
        if e * d % tot == 1:
        
            return d
        d += 1
        

        




lista = creates_pnumbers(100)
p, q, n = product(lista)
tot = totiente(p, q, n)
coprimos = co_primos(p, q, n, tot)
e = sample(coprimos, 1) #Seleciona um numero aleatório entre os coprimos de N. O 'e' é a chave pública
a = private_key(e[0], tot)
print(a)
print(e[-1])
print(tot)
print(p, q, n, tot, e[0], a)