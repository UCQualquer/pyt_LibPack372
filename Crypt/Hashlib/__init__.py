from argon2 import PasswordHasher, extract_parameters, Parameters
from argon2.exceptions import VerifyMismatchError


# i would recommend using Argon2

class Argon2(object):
    def __init__(self, time_cost: int = 8, memory_cost: int = 102400, parallelism: int = 8, hash_len: int = 64, salt_len: int = 128):
        self.ph = PasswordHasher(time_cost = time_cost, memory_cost = memory_cost, parallelism = parallelism, hash_len = hash_len, salt_len = salt_len)
        pass

    def create_hash(self, data: str) -> str:
        return self.ph.hash(data)
    
    def verify(self, hash: str, data: str) -> bool:
        """Verify if already hashed [hash] is equals to unhashed [data].

        Args:
            hash (str): An Argon2 hashed value, normally stored in a database.
            data (str): A [str] to verify,  it will be hashed using [hash] parameteres then will be compared;

        Returns:
            bool: return [True] if [data] that was encrypted using [hash]s crypt parameters is equals to [hash], else [False]
        """
        try:
            return self.ph.verify(hash, data)
            
        except VerifyMismatchError:
            return False
    
    def needs_rehash(self, hash) -> bool:
        return self.ph.check_needs_rehash(hash)
    
    def extract_parameters(self, hash: str) -> Parameters:
        return extract_parameters(hash)