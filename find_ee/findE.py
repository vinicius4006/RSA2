def find_e(d: int, z: int) -> int:
    e = 1
    while True:
       
        if pow(d, e, z) == 1:
            return e
        e += 1
        
