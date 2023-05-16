def euclidean_extended_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = euclidean_extended_algorithm(b, a % b)
        x_new = y
        y_new = x - (a // b) * y
        return gcd, x_new, y_new

def find_d(e, p_n):
    gcd, x, _ = euclidean_extended_algorithm(e, p_n)
    d = x % p_n
    return d

# Exemplo de utilização:
e = 17  # Valor de E
p_n = 80  # Valor de φ(n)

def main():
    d = find_d(e, p_n)
    return d

d_value = main()
print("O valor de D que satisfaz a condição é:", d_value)
