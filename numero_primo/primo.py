import math

def is_prime(num):
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

a = is_prime(98764321261)
print(a)