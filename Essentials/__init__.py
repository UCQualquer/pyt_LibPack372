from My_Pack.System import bruteCls as cls
from My_Pack.Crypt import generateRandomToken as grt
from requests import Session as __Session
from typing import Dict, List, Tuple, Union, Any
import os, json, sys

rq = __Session()
rq.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def isNone(data) -> bool: return data is None
def isNotNone(data) -> bool: return not (data is None)

def isType(object: object, _class: object) -> bool:
    return issubclass(object, _class) if type(object) == type else issubclass(type(object), _class)

def ensureType(object: object, _class: object, name: str = None):
    if isNone(name):
        name = 'Argument'
    
    else:
        name = f'[{name.strip("[").strip("]")}]'

    if not isType(object, _class):
        raise TypeError(f'{name} is expected to be type {_class}, but got {type(object)}.')

def removeDuplicates(l: list) -> list:
    return list(dict.fromkeys(l))

def leftPad(text: str, mul: int, char: str) -> str:
    if len(char) > 1: raise ValueError('[Char] lenght should be exactly 1')

    return ((mul - len(text) % mul) * char) + text


def rightPad(text: str, mul: int, char: str) -> str:
    if len(char) > 1: raise ValueError('[Char] lenght should be exactly 1')

    return text + ((mul - len(text) % mul) * char)

def LoadJson(file_path: str, default = {}):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        r = f.read()
    return json.loads(r) if r else default
ReadJson = LoadJson

def WriteJson(file_path: str, object_: object):
    with open(file_path, 'w', encoding = 'utf-8') as f:
        json.dump(object_, f, indent = 4, ensure_ascii = False)

def chunkate(obj: Union[tuple, list], items_per_chunk: int) -> List[list]:
    for i in range(0, len(obj), items_per_chunk):
        yield obj[i:i + items_per_chunk]

def chunkate2(obj: Union[tuple, list], chunks: int) -> List[list]:
    k, m = divmod(len(obj), chunks)
    for i in range(chunks):
        yield obj[i * k + min(i, m):(i+1) * k + min(i+1, m)] # https://stackoverflow.com/a/2135920/10996607


