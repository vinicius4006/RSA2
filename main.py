import numero_primo.primo as p
import find_NZ.find_n_z as fnz
import find_d.Dprimo as fd
import find_ee.findE as fe

# Passar um intervalo especifico e tentar encontrar um primo
P = p.generate_prime_number(7, 23) # Primeiro intervalo
Q = p.generate_prime_number(11, 50) # Segundo intervalo
print(P)
print(Q)

# Adquirir N e Z
N = fnz.calculate_N(P, Q)
Z = fnz.calculate_Z(P, Q)
print(N)
print(Z)

# Adquirir D, coprimo de Z
D = fd.co_primos(P, Q, Z)
print(D)

# Adquirir E, produto 
E = fe.find_E(D, Z)
print(E)