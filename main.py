import numero_primo.primo as p
import find_NZ.find_n_z as fnz
import find_d.Dprimo as fd


# Passar um intervalo especifico e tentar encontrar um primo
P = p.generate_prime_number(15000000, 16000000) # Primeiro intervalo
Q = p.generate_prime_number(1100000, 5000000) # Segundo intervalo
print(P)
print(Q)

# Adquirir N e Z
N = fnz.calculate_N(P, Q)
Z = fnz.calculate_Z(P, Q)
print(N)
print(Z)


# Adquirir D, coprimo de Z
