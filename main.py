import numero_primo.primo as p
import find_NZ.find_n_z as fnz
import find_d.Dprimo as fd
import find_ee.findE as fe

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

def string_to_int(message):
    
    message = ''.join(format(ord(c), '08b') for c in message)
    return int(message, 2)

print(string_to_int('Olá, mundo!'))

def cifrar(message, E, N):
    
    message = string_to_int(message)
    cifra = message ** E % N
    return cifra

message = 'Olá Mundo'    
cifra = cifrar(message, E, N)
    

# Decifrar

def int_to_string(message):
    binary = format(message, 'b')
    chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''.join(chr(int(chunk, 2)) for chunk in chunks)
    return message
    
def decifrar(cifra, D, N):
    
    decifra = cifra ** D % N
    message = int_to_string(decifra)
    return message

message = decifrar(cifra, D, N)
print(message)
