import random as __random

def randomIp() -> str:
    return '.'.join([str(__random.randint(1, 255)) for _ in range(4)])