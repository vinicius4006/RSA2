def euclidean_extended_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = euclidean_extended_algorithm(b, a % b)
        x_new = y
        y_new = x - (a // b) * y
        return gcd, x_new, y_new

def find_e(d, z):
    _, x, _ = euclidean_extended_algorithm(d, z)
    e = x % z
    return e
        
    
print(find_e(209, 271))
