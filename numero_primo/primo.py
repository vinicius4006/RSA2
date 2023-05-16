def is_prime(num):
    result = False
    if num <= 1:
        return result
    if num <= 3 or num == 5 or num == 7:
        result = True
        return result
    
    if is_two(num):
        return result
    
    if is_three(num):
        return result
    
    if is_five(num):
        return result
    
    if is_seven(num):
        return result
    
    denominator = 11
    quotient = num // denominator
    stop = False
    
    while True:
        if stop:
            break
        if quotient < denominator:
            stop = True
            result = True
        if num % denominator == 0:
            stop = True
        else:
            denominator += 1
    
    return result


def is_two(num):
    return num % 2 == 0


def is_three(num):
    s = list(str(num))
    soma = sum(int(digit) for digit in s)
    return soma % 3 == 0


def is_five(num):
    s = list(str(num))
    return s[-1] == "5" or s[-1] == "0"


def is_seven(num):
    return num % 7 == 0


a = is_prime(14615016373309029182036848327162830196559325429763531029354160528133907320308105037998849027227)

print(a)