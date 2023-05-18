import math
import random

def is_prime(num):
    """ Verifica se um numero é primo"""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    # Verificar divisibilidade apenas até a raiz quadrada do número
    sqrt_num = int(math.sqrt(num)) + 1
    for divisor in range(5, sqrt_num, 6):
        if num % divisor == 0 or num % (divisor + 2) == 0:
            return False

    return True


def generate_prime_number(inicio, fim):
        stop = True 
        num_prime = 2
        while stop:
             new_num = random.randint(inicio, fim)
             if is_prime(new_num):
                  num_prime = new_num
                  stop = False
        return num_prime


