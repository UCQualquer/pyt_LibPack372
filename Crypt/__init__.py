import secrets

def generateRandomToken(size: int = 32) -> str:
    return secrets.token_urlsafe(size)[:size]

def generateRandomByteToken(size: int = 32) -> bytes:
    return secrets.token_bytes(size)[:size]