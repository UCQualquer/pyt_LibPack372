from .Url import Url
from .File import File

def sortDict(obj: dict) -> dict:
    def sort(x):
        return sorted(x, key = lambda _x: _x.lower())

    # Sort keys
    obj = {k: obj[k] for k in sort(obj.keys())}

    # Sort values
    for key, val in obj.items():
        if type(val) in (list, set, tuple):
            obj[key] = sortList(val)

        elif type(val) in (dict,):
            obj[key] = sortDict(val)
    return obj

def sortList(obj: list) -> list:
    if all(type(i) == str for i in obj):
        return sorted(obj, key = lambda x: x.lower())

    elif all(type(i) == int for i in obj):
        return sorted(obj, key = lambda x: x)

    for pos, val in enumerate(obj):
        if type(val) in (list, set, tuple):
            obj[pos] = sortList(val)
        elif type(val) in (dict,):
            obj[pos] = sortDict(val)
    return obj

from typing import List

def removeDuplicates(x: List[str]) -> List[str]:
    return list(dict.fromkeys(x))

def listStrip(x: List[str], str_: str = ' ') -> List[str]:
    return [i.strip(str_) for i in x]