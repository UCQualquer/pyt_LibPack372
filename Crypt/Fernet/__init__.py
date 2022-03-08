import base64, hashlib

from cryptography.fernet import Fernet as Fern

class Fernet(object):
    def __init__(self, key: bytes = None):
        if not key:
            key = Fernet.generate_key()
        self.fernet = Fern(key)

    def encrypt(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)
    
    def decrypt(self, data: bytes) -> bytes:
        return self.fernet.decrypt(data)

    def encrypt_at_time(self, data: bytes, time: int) -> bytes:
        return self.fernet.encrypt_at_time(data, time)

    def decrypt_at_time(self, data: bytes, ttl: int, time: int) -> bytes:
        return self.fernet.decrypt_at_time(data, ttl, time)

    def extract_timestamp(self, token: bytes) -> int:
        return self.fernet.extract_timestamp(token)

    @staticmethod
    def generate_key() -> bytes:
        return Fern.generate_key()
    
    @staticmethod
    def generate_key_from_string(string: str) -> bytes:
        return base64.urlsafe_b64encode(hashlib.sha256(string.encode('utf-8')).digest())