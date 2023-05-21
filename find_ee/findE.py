def find_e(d: int, z: int) -> int:
    e = 1
    while True:
       
        if d * e % z == 1:
        
            return e
        e += 1
        
