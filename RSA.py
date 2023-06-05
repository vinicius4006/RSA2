#Importe das bilbiotecas 
import math
import random
from random import sample
import base64
import json


def mdc(n1: int, n2: int) -> int:
    """Recebe dois números e retorna o MDC deles"""

    while n2:
        n1, n2 = n2, n1 % n2
    return n1


def co_primos(z:int) -> int:
    """Verifica se dois números são coprimos"""

    b = 1
    coprimos = []
    while len(coprimos) < z:
        res = mdc(z, b)         #Obtem o MDC chamando a função mdc()
        if res == 1:        
            coprimos.append(b)
        b += 1

    d = sample(coprimos, 1)     #Entre todos os coprimos Z, seleciona um deles 
    return int(d[0])            #aleatoriamente


def find_e(d: int, z: int) -> int:
    """Dado D e Z, encontra E"""

    e = 1
    while True:
        if d * e % z == 1:
            return e
        e += 1


def calculate_N(P, Q):
    """Calcula N, produto de dois números primos"""

    N = P * Q
    return N


def calculate_Z(P, Q):
    """Calcula Z, produto de (P-1) e (Q-1)"""

    Z = (P - 1) * (Q - 1)
    return Z


def is_prime(num):
    """Verifica se determinando número é primo"""

    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    sqrt_num = int(math.sqrt(num)) + 1
    for divisor in range(5, sqrt_num, 6):
        if num % divisor == 0 or num % (divisor + 2) == 0:
            return False

    return True


def generate_prime_number(inicio, fim):
    """Gera numeros primos. Dado um intervalo especificado, seleciona
    aleatoriamente um número desse intervalo e verifica se é primo com
    a chamada de is_prime()"""

        stop = True 
        num_prime = 2
        while stop:
             new_num = random.randint(inicio, fim) #número aleatório dentro do intervalo
             if is_prime(new_num):                 #verifica com is_prime()
                  num_prime = new_num
                  stop = False
        return num_prime
    

def generate_keys(range_in, range_out):
    """Retorna as chaves públicas e privadas"""

    #chamadas as funções especificas acima
    p = generate_prime_number(range_in, range_out) 
    q = generate_prime_number(range_in, range_out) 
    n = calculate_N(p, q)
    z = calculate_Z(p, q)
    d = co_primos(z)
    e = find_e(d, z)

    #chaves pública e privada
    public_key, private_key = [e, n], [d, n]
    return public_key, private_key


def encrypt(message, public_key):
    """Recebe a mensagem  e a chave pública para criptografar a mensagem.
    A mensagem é criptografada letra por letra usando as chaves"""

    e, n = public_key
    encrypt_list = [pow(ord(char.encode("latin1")), e, n) for char in message]
    encrypt_list = str(encrypt_list)
    return base64.b64encode(encrypt_list.encode('UTF-8'))


def decrypt(encrypt_list, private_key):
    """Recebe a mensagem criptografada e a chave privada. Em conjunto com 
    a chave privada, faz o processo inverso da função encrypt() para 
    descriptografar a mensagem"""

    encrypt_list = list(json.loads(str(base64.b64decode(encrypt_list))[2:-1]))
    d, n = private_key
    message = ''.join([chr(pow(char, d, n)) for char in encrypt_list])
    return message
