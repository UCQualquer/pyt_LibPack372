from My_Pack.Essentials import ensureType, Tuple
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

""" Use example:
from My_Pack.Crypt.RSA import *

pub, priv = createKeys()

message = 'mensagem'.encode('utf-8')
enc = encrypt(message, pub)
dec = decrypt(enc, priv)

print(dec) # b'mensagem'
"""

""" Decription:
    Uses RSA to encrypt data.

    Public keys can only be used to encrypt data.
    Private keys can only be used to decrypt data.

    No matter who haves the public keys.
    Secure your private key with your soul and being.
"""



def createKeys(size: int = 2048, as_pem: bool = False) -> Tuple[bytes, bytes]:
    """ Create random RSA keys.

    Args:
        size (int, optional): Private key's size. Defaults to 2048.
        as_pem (bool, optional): True to return key with PEM headers. Defaults to False.

    Returns:
        Tuple[bytes, bytes]: Returns a tuple with the public and private key.
    """

    ensureType(size, int, 'size')
    ensureType(as_pem, int, 'as_pem')

    p_key: rsa.RSAPrivateKey = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = size
    )

    public_key: bytes = p_key.public_key().public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.PKCS1
    ).strip(b'\n')
    private_key: bytes = p_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = serialization.NoEncryption()
    ).strip(b'\n')

    if as_pem == False:
        public_key = b''.join(public_key.split(b'\n')[1:-1])
        private_key = b''.join(private_key.split(b'\n')[1:-1])
    return (public_key, private_key)

def encrypt(data: bytes, public_key: bytes) -> bytes:
    """ Encrypts [data] using [public_key].

    Args:
        data (bytes): Data to be encrypted.
        public_key (bytes): A valid RSA public key. Should look like the ones stored in .pem files.

    Returns:
        bytes: Encrypted data.
    """

    ensureType(data, bytes, 'data')
    ensureType(public_key, bytes, 'public_key')

    if not public_key.startswith(b'-----BEGIN RSA PUBLIC KEY-----\n'):
        public_key = b'-----BEGIN RSA PUBLIC KEY-----\n' + public_key

    if not public_key.endswith(b'\n-----END RSA PUBLIC KEY-----'):
        public_key += b'\n-----END RSA PUBLIC KEY-----'

    public_key = serialization.load_pem_public_key(public_key)
    alg = hashes.SHA256()
    pad = padding.OAEP(
            mgf = padding.MGF1(algorithm = alg),
            algorithm = alg,
            label = None
        )

    encrypted = public_key.encrypt(data, pad)

    return encrypted


def decrypt(data: bytes, private_key: bytes) -> bytes:
    """ Decrypts [data] using [private_key].

    Args:
        data (bytes): Data to be decrypted.
        private_key (bytes): A valid RSA private key. Should look like the ones stored in .pem files.

    Returns:
        bytes: Decrypted data.
    """

    ensureType(data, bytes, 'data')
    ensureType(private_key, bytes, 'private_key')

    if not private_key.startswith(b'-----BEGIN PRIVATE KEY-----\n'):
        private_key = b'-----BEGIN PRIVATE KEY-----\n' + private_key

    if not private_key.endswith(b'\n-----END PRIVATE KEY-----'):
        private_key += b'\n-----END PRIVATE KEY-----'

    private_key = serialization.load_pem_private_key(private_key, None)
    alg = hashes.SHA256()
    pad = padding.OAEP(
            mgf = padding.MGF1(algorithm = alg),
            algorithm = alg,
            label = None
        )
    decrypted = private_key.decrypt(data, pad)

    return decrypted