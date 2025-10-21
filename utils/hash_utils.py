import hashlib

def md5_hash(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()

def sha256_hash(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def hash_to_bytes(hash_str):
    return bytes.fromhex(hash_str)
