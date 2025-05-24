#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
config.py
=========
ملف إعدادات المشروع يحتوي على متغيرات التهيئة الأساسية
"""

import os
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env (إذا كان موجودًا)
load_dotenv()

# مسار تخزين البيانات والملفات
BASE_DIR = Path(os.getenv("BASE_DIR", "C:/Manhal/Manhal_ai"))
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# توليد مفتاح تشفير فريد (إذا لم يكن متاحًا مسبقًا)
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = Fernet.generate_key().decode()
    with open(BASE_DIR / "secret.key", "w") as f:
        f.write(SECRET_KEY)

# إعدادات قاعدة البيانات
DB_NAME = "manhal_ai.db"
DB_PATH = DATA_DIR / DB_NAME

# إعدادات نموذج التعلم العميق
MODEL_NAME = "bert-base-arabic"
NLP_THRESHOLD = 0.8  # حد الدقة لتحليل النصوص

# إعدادات الأمان
ENABLE_2FA = True  # تفعيل المصادقة الثنائية
ENCRYPTION_ALGORITHM = "AES-256"
HASH_ALGORITHM = "SHA-512"

# إنشاء المجلدات إذا لم تكن موجودة
for directory in [DATA_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

print(f"تم تحميل الإعدادات بنجاح من {BASE_DIR}")