__version__ = "2.1.0"  # توافق مع نظام المفاتيح الجديد

import sqlite3
import logging
from pathlib import Path
from cryptography.fernet import Fernet
from .config import SECRET_KEY, DATA_DIR

class DatabaseManager:
    def __init__(self, db_name: str = "manhal.db"):
        self.db_path = DATA_DIR / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # التعديل هنا: استخدام SECRET_KEY مباشرة
        self.cipher = Fernet(SECRET_KEY)
        
        self._initialize_tables()

    def _initialize_tables(self):
        """إنشاء الجداول الأساسية"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except Exception as e:
            logging.error(f"خطأ في إنشاء الجداول: {str(e)}")
            raise

    def save_document(self, title: str, content: str):
        """حفظ المستند مع التشفير"""
        try:
            encrypted_content = self.cipher.encrypt(content.encode())
            self.cursor.execute(
                "INSERT INTO documents (title, content) VALUES (?, ?)",
                (title, encrypted_content)
            )
            self.conn.commit()
        except Exception as e:
            logging.error(f"خطأ في حفظ المستند: {str(e)}")
            raise

    def get_document(self, doc_id: int) -> str:
        """استرجاع المستند مع فك التشفير"""
        try:
            self.cursor.execute("SELECT content FROM documents WHERE id=?", (doc_id,))
            row = self.cursor.fetchone()
            if row:
                return self.cipher.decrypt(row[0]).decode()
            return ""
        except Exception as e:
            logging.error(f"خطأ في استرجاع المستند: {str(e)}")
            raise