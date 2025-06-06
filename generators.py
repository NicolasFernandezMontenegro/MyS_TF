from collections.abc import Generator


def genCongruencial(seed: int, a: int, c: int, mod: int) -> Generator[int, None, None]:
    while True:
        seed = (a * seed + c) % mod
        yield seed / mod

def XorShift(seed: int) -> Generator[int, None, None]:
    while True:
        seed ^= (seed << 13)
        seed ^= (seed >> 17)
        seed ^= (seed << 5)
        seed = seed & 0xFFFFFFFF
        yield seed  / 2**32 
        


def initState(seed: int, n: int, w: int, f:int) -> list[int]:
    mt = [0] * n
    mt[0] = seed & 0xFFFFFFFF
    for i in range(1, n):
        mt[i] = (f * (mt[i - 1] ^ (mt[i - 1] >> (w - 2))) + i) & 0xFFFFFFFF
    return mt




def Mersenne(seed: int) -> Generator[int, None, None]:
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908B0DF
    u, s, t, l = 11, 7, 15, 18
    f = 1812433253
    b = 0x9D2C5680
    c = 0xEFC60000
    UMASK = 0x80000000
    LMASK = 0x7FFFFFFF
    FULL_MASK = 0xFFFFFFFF

    mt = initState(seed, n, w,f)
    index = n

    while True:
        if index >= n:
            for i in range(n):
                x = (mt[i] & UMASK) | (mt[(i + 1) % n] & LMASK)
                xA = x >> 1
                if x % 2 != 0:
                    xA ^= a
                mt[i] = mt[(i + m) % n] ^ xA
            index = 0

        y = mt[index]
        
        y ^= (y >> u) & FULL_MASK
        y ^= (y << s) & b
        y ^= (y << t) & c
        y ^= (y >> l)

        index += 1
        yield y  / 2**w 

if __name__ == "__main__":
    generador = genCongruencial(1, 16807, 0, 2**31 - 1)
    for _ in range(10):
        print(next(generador))

    generador_xor = XorShift(1)
    for _ in range(10):
        print(next(generador_xor))

    generador_mersenne = Mersenne(1)
    for _ in range(10):
        print(next(generador_mersenne))
