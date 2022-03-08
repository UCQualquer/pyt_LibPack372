import base64 as b64
from Crypto.Cipher import AES
from My_Pack.Crypt import generateRandomByteToken as grbt
from My_Pack.Essentials import ensureType, Tuple

""" Use example:
from My_Pack.Crypt.RSA import *

key = os.urandom(32)

message = 'mensagem'.encode('utf-8')
enc = encrypt(message, key)
dec = decrypt(enc, key)

print(dec) # b'mensagem'
"""

""" Decription:
    Uses AES to encrypt data.
"""


def createKey(size: int = 32, as_pem: bool = False) -> bytes:
    """ Create random AES key.

    Args:
        size (int, optional): Key's size. Can be 16, 24 or 32. Defaults to 32.

    Returns:
        bytes: [size] bytes long AES key.
    """

    ensureType(size, int, 'size')
    return grbt(size)


def encrypt(data: bytes, key: bytes) -> bytes:
    """ Encrypts [data] using [key].
    The encryption method depends on [key] lenght: 16, 24 or 32 for AES 128, 192 or 256, respectively.

    Args:
        data (bytes): Byte data to be encrypted.
        key (bytes): 16, 24 or 32 bytes long encryption key.

    Raises:
        ValueError: Raises if [key]'s len is unsupported.

    Returns:
        bytes: Encrypted [data].
    """

    ensureType(data, bytes, 'data')
    ensureType(key, bytes, 'key')
    
    if not (len(key) in (16, 24, 32)):
        raise ValueError(f'[key] must be 16, 24 or 32 bytes long')

    encrypted_data = __aesEncrypt(data, key)
    return encrypted_data

def decrypt(data: bytes, key: bytes) -> bytes:
    """ Decrypts [data] using [key].

    Args:
        data (bytes): Byte data to be decrypted.
        key (bytes): 16, 24 or 32 bytes long encryption key.

    Raises:
        ValueError: Raises if [key]'s len is unsupported.

    Returns:
        bytes: Decrypted [data]
    """

    ensureType(data, bytes, 'data')
    ensureType(key, bytes, 'key')

    if not (len(key) in (16, 24, 32)):
        raise ValueError(f'[key] must be 16, 24 or 32 bytes long')

    decrypted_data = __aesDecrypt(data, key)
    return decrypted_data


def __aesEncrypt(data: bytes, key: bytes) -> bytes:
    # Set block_size. AES only supports multiples of 16
    BS = 16

    # [pad] function, that fills the remaining spaces to make the data len multiple of 16.
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode('utf-8')
    data = pad(data)

    # Creates an initialization vector. Its use remains blurry in my head.
    iv = grbt(16)

    # Creates AES object with [key], mode and [iv]. After, encrypts [data].
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(data)

    # Return an urlsafe sum of [iv] and [encrypted]
    return iv + encrypted

def __aesDecrypt(data: bytes, key: bytes) -> bytes:
    # Set block_size. AES only supports multiples of 16
    BS = 16

    # [unpad] function, that remove the padding used to make the data len multiple of 16
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # Gets the initialization vector
    iv = data[:BS]
    data = data[BS:]

    # Creates AES object with [key], mode and [iv]. After, decrypts [data].
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(data)

    # Returns unpaded [decrypted]
    return unpad(decrypted)