__version__ = "2.1.0"  # دعم Fernet مع PBKDF2

from pathlib import Path
import os
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# إعداد المسارات
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / ".config"

# إنشاء المجلدات
for folder in [DATA_DIR, CONFIG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

class KeyManager:
    def __init__(self):
        self.key_path = CONFIG_DIR / "fernet.key"
        self.salt = b'fixed_salt_for_consistency'  # يجب تغييره في الإنتاج
        
        if not self.key_path.exists():
            self._generate_fernet_key()

    def _generate_fernet_key(self):
        """توليد مفتاح Fernet صالح (32 بايت)"""
        try:
            # توليد مفتاح 32 بايت مناسب لـ Fernet
            password = os.getenv("MANHAL_SECRET", "default-secret-key").encode()
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=default_backend()
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            with open(self.key_path, "wb") as f:
                f.write(key)
                
        except Exception as e:
            logging.critical(f"فشل توليد المفتاح: {str(e)}")
            raise

    def get_fernet_key(self) -> bytes:
        """الحصول على مفتاح Fernet"""
        with open(self.key_path, "rb") as f:
            return f.read()

# التهيئة
try:
    key_manager = KeyManager()
    SECRET_KEY = key_manager.get_fernet_key()
except Exception as e:
    logging.critical(f"فشل تحميل المفتاح: {str(e)}")
    exit(1)