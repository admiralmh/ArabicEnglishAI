#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
security.py
==================
نظام الأمان المتقدم لحماية البيانات عبر التشفير والمصادقة الثنائية
"""

import os
import hashlib
import hmac
import logging
import base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ..config import SECRET_KEY, DATA_DIR

class SecurityManager:
    """
    وحدة الأمان المتقدمة لتشفير البيانات والتحقق من تكامل المستندات
    """

    def __init__(self):
        self.secret_key = SECRET_KEY.encode()
        self.salt = b"random_salt_value"
        self.encryption_key = self._derive_key(self.secret_key, self.salt)
        logging.info("تم تهيئة نظام الأمان بنجاح.")

    def _derive_key(self, key: bytes, salt: bytes) -> bytes:
        """
        اشتقاق مفتاح قوي للتشفير باستخدام PBKDF2
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(key)

    def encrypt_data(self, plaintext: str) -> str:
        """
        تشفير النصوص باستخدام `AES-256`
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data).decode()

    def decrypt_data(self, encrypted_text: str) -> str:
        """
        فك تشفير النصوص باستخدام `AES-256`
        """
        data = base64.b64decode(encrypted_text)
        iv, encrypted_data = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_data) + decryptor.finalize()

    def sign_file(self, file_path: Path) -> str:
        """
        إنشاء توقيع رقمي للمستند باستخدام `SHA-512` للتحقق من سلامته
        """
        with open(file_path, "rb") as f:
            file_data = f.read()
        return hashlib.sha512(file_data).hexdigest()

    def verify_file_integrity(self, file_path: Path, expected_hash: str) -> bool:
        """
        التحقق من سلامة الملف عبر مقارنة توقيعه الرقمي
        """
        actual_hash = self.sign_file(file_path)
        return hmac.compare_digest(actual_hash, expected_hash)

# اختبار عملي للكود
if __name__ == "__main__":
    security = SecurityManager()
    
    # تجربة التشفير وفك التشفير
    encrypted_text = security.encrypt_data("هذا نص سري للغاية")
    print(f"نص مشفر: {encrypted_text}")
    decrypted_text = security.decrypt_data(encrypted_text)
    print(f"نص مفكوك التشفير: {decrypted_text}")

    # تجربة توقيع الملف والتحقق منه
    sample_file = Path("C:/Manhal/Manhal ai/data/sample.txt")
    file_hash = security.sign_file(sample_file)
    print(f"توقيع الملف: {file_hash}")
    integrity_check = security.verify_file_integrity(sample_file, file_hash)
    print(f"هل الملف سليم؟ {'نعم' if integrity_check else 'لا'}")