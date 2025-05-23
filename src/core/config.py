__version__ = "3.0.0"  # إصدار كامل مع جميع التعديلات

import base64
import os
import logging
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ------ إعداد المسارات الأساسية ------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / ".config"
LOGS_DIR = BASE_DIR / "logs"

# ------ إنشاء المجلدات الضرورية ------
for folder in [DATA_DIR, CONFIG_DIR, LOGS_DIR]:
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.critical(f"فشل إنشاء مجلد {folder}: {str(e)}")
        raise

# ------ تهيئة نظام التسجيل ------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

# ------ نظام إدارة المفاتيح الآمن ------
class KeyManager:
    def __init__(self):
        self.key_path = CONFIG_DIR / "fernet.key"
        self.salt = b'manhal_salt_2024'  # يجب تغييره في بيئة الإنتاج
        
        if not self.key_path.exists():
            self._generate_fernet_key()

    def _generate_fernet_key(self):
        """توليد مفتاح Fernet صالح باستخدام PBKDF2"""
        try:
            # استخدام كلمة مرور من متغيرات البيئة أو افتراضية
            password = os.getenv("MANHAL_SECRET", "default-secret-1234").encode()
            
            # توليد المفتاح باستخدام خوارزمية PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=default_backend()
            )
            
            # توليد وتشفير المفتاح
            key_material = kdf.derive(password)
            fernet_key = base64.urlsafe_b64encode(key_material).decode('utf-8')
            
            # حفظ المفتاح في ملف
            with open(self.key_path, "w", encoding="utf-8") as f:
                f.write(fernet_key)
                
            logging.info("تم توليد مفتاح تشفير جديد بنجاح")
            
        except Exception as e:
            logging.error(f"فشل توليد المفتاح: {str(e)}")
            raise

    def get_fernet_key(self) -> bytes:
        """استرجاع مفتاح Fernet"""
        try:
            with open(self.key_path, "r", encoding="utf-8") as f:
                key = f.read().strip()
                return key.encode('utf-8')
        except Exception as e:
            logging.error(f"فشل قراءة المفتاح: {str(e)}")
            raise

# ------ التهيئة الرئيسية للنظام ------
try:
    logging.info("جاري تهيئة نظام التشفير...")
    key_manager = KeyManager()
    SECRET_KEY = key_manager.get_fernet_key()
    logging.info("تم التهيئة بنجاح")
except Exception as e:
    logging.critical(f"فشل حرج في التهيئة: {str(e)}")
    exit(1)