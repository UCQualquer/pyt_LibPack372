import os
from typing import List

def cls():
    os.system('cls||clear')

def bruteCls():
    if os.name in ('posix'):
        os.system('clear')

    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')

    else:
        printCls2()

def printCls():
    print('\033c')

def printCls2():
    print('\x1b[2J\x1b[;H', end = '')

def split(string: str, keep_quoted = True, *args, **kwargs) -> List[str]:
    if keep_quoted:
        import shlex
        return shlex.split(string, *args, **kwargs)
    
    else:
        return string.split(*args, **kwargs)

