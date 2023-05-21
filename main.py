import numero_primo.primo as p
import find_NZ.find_n_z as fnz
import find_d.Dprimo as fd
import find_ee.findE as fe

def string_to_int(message):
    binary_list = []
    for c in message:
        binary = format(ord(c), '08b')
        binary_list.append(binary)

    binary_string = ''.join(binary_list)
    return int(binary_string, 2)

def make_divisible_by_eight(binary):
    remainder = len(binary) % 8
    if remainder != 0:
        binary = '0' * (8 - remainder) + binary
    return binary

def int_to_string(message):
    binary = format(message, 'b')
    binary = make_divisible_by_eight(binary)
    chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''.join(chr(int(chunk, 2)) for chunk in chunks)
    return message

def binary_to_bytes(binary_list):
    bytes_data = bytes([int(binary, 2) for binary in binary_list])
    return bytes_data
    
def decifrar(cifra, D, N):
    decifra = (cifra ** D) % N
    message = int_to_string(decifra)
    return message

def cifrar(message, E, N):
    message = string_to_int(message)
    cifra = (message ** E) % N
    return cifra

# Passar um intervalo especifico e tentar encontrar um primo
P = p.generate_prime_number(75, 230) # Primeiro intervalo
Q = p.generate_prime_number(118, 500) # Segundo intervalo
print(P)
print(Q)

# Adquirir N e Z
N = fnz.calculate_N(P, Q)
Z = fnz.calculate_Z(P, Q)
print(N)
print(Z)

# Adquirir D, coprimo de Z
D = fd.co_primos(Z)
print(D)

# Adquirir E
E = fe.find_e(D, Z)
print(E)

# Cifrar
message = 'Olá Mundo'    
cifra = cifrar(message, E, N)
    
# Decifrar
message = decifrar(cifra, D, N)
print(message)
print(int_to_string(string_to_int('OOOláaaa, mundo')))



