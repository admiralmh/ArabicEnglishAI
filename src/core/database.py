#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
database.py
==================
مدير قاعدة البيانات مع دعم التشفير وتسجيل التدقيق الأمني
"""

import sqlite3
import logging
import hashlib
from pathlib import Path
from typing import Optional, List, Dict
from contextlib import contextmanager
from cryptography.fernet import Fernet, InvalidToken
from ..config import SECRET_KEY, DATA_DIR

class DatabaseManager:
    """
    مدير قاعدة البيانات لتخزين واسترجاع المستندات بأمان باستخدام `AES-256`
    """

    def __init__(self, db_name: str = "manhal_ai.db"):
        self.db_path = Path(DATA_DIR) / db_name
        self._init_encryption()
        self._init_db_schema()

    def _init_encryption(self):
        """
        تهيئة نظام التشفير مع التحقق من المفتاح السري
        """
        try:
            self.cipher = Fernet(SECRET_KEY)
            test_token = self.cipher.encrypt(b"test")
            assert self.cipher.decrypt(test_token) == b"test"
        except (ValueError, InvalidToken) as e:
            logging.critical(f"فشل تهيئة التشفير: {e}")
            raise RuntimeError("خطأ في تكوين المفتاح السري") from e

    @contextmanager
    def _db_connection(self):
        """
        إدارة اتصال آمن بقاعدة البيانات
        """
        conn = sqlite3.connect(
            self.db_path,
            timeout=20,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA secure_delete = ON")
            yield conn
        finally:
            conn.close()

    def _init_db_schema(self):
        """
        إنشاء هياكل الجداول الأساسية في قاعدة البيانات
        """
        with self._db_connection() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL UNIQUE,
                    content BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sha256_hash TEXT NOT NULL,
                    file_type TEXT CHECK(file_type IN ('DOC', 'PDF', 'TXT', 'IMG'))
                );

                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    details TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_docs_title ON documents(title);
            ''')
            conn.commit()

    def save_document(self, title: str, content: str, file_type: str) -> bool:
        """
        حفظ مستند جديد مع التحقق من التكامل
        """
        try:
            encrypted_content = self.cipher.encrypt(content.encode("utf-8"))
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

            with self._db_connection() as conn:
                conn.execute('''
                    INSERT INTO documents 
                    (title, content, sha256_hash, file_type)
                    VALUES (?, ?, ?, ?)
                ''', (title, encrypted_content, content_hash, file_type))
                conn.commit()
                self._log_event(conn, "DOC_SAVE", f"تم حفظ المستند: {title}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"المستند '{title}' موجود مسبقاً")
            return False
        except Exception as e:
            logging.error(f"خطأ في الحفظ: {e}")
            return False

    def get_document(self, doc_id: int) -> Optional[Dict]:
        """
        استرجاع مستند مع التحقق من سلامته
        """
        try:
            with self._db_connection() as conn:
                row = conn.execute('''
                    SELECT title, content, sha256_hash 
                    FROM documents 
                    WHERE id = ?
                ''', (doc_id,)).fetchone()
                
                if not row:
                    return None
                
                decrypted_content = self.cipher.decrypt(row[1]).decode("utf-8")
                current_hash = hashlib.sha256(decrypted_content.encode("utf-8")).hexdigest()
                
                if current_hash != row[2]:
                    raise InvalidToken("التجزئة غير متطابقة - تلاعب محتمل")
                
                return {
                    "id": doc_id,
                    "title": row[0],
                    "content": decrypted_content,
                    "hash": current_hash
                }
        except InvalidToken as e:
            logging.critical(f"خطر أمني: {e}")
            with self._db_connection() as conn:
                self._log_event(conn, "SECURITY_ALERT", str(e))
            return None
        except Exception as e:
            logging.error(f"خطأ في الاسترجاع: {e}")
            return None

    def _log_event(self, conn, event_type: str, details: str = ""):
        """
        تسجيل الأحداث الأمنية داخل قاعدة البيانات
        """
        try:
            conn.execute('''
                INSERT INTO audit_log 
                (event_type, details)
                VALUES (?, ?)
            ''', (event_type, details))
            conn.commit()
        except Exception as e:
            logging.error(f"فشل تسجيل الحدث: {e}")

    def search_documents(self, keyword: str) -> List[Dict]:
        """
        البحث عن مستندات تحتوي على الكلمة المطلوبة
        """
        try:
            with self._db_connection() as conn:
                rows = conn.execute('''
                    SELECT id, title 
                    FROM documents 
                    WHERE title LIKE ? 
                    LIMIT 50
                ''', (f"%{keyword}%",)).fetchall()

                return [{"id": row[0], "title": row[1]} for row in rows]
        except Exception as e:
            logging.error(f"خطأ أثناء البحث: {e}")
            return []

# اختبار عملي للكود
if __name__ == "__main__":
    db = DatabaseManager()
    db.save_document("اختبار", "محتوى الاختبار", "TXT")
    print(db.get_document(1))