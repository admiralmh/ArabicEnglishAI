import hashlib
import os

class Security:
    def __init__(self, key_path="secret.key"):
        self.key_path = key_path
        self.key = self.load_or_create_key()

    def load_or_create_key(self):
        if not os.path.exists(self.key_path):
            key = os.urandom(32)
            with open(self.key_path, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_path, 'rb') as f:
                key = f.read()
        return key

    def hash_password(self, password):
        return hashlib.sha256((password + self.key.hex()).encode()).hexdigest()

    def verify_password(self, password, hashed):
        return self.hash_password(password) == hashed
