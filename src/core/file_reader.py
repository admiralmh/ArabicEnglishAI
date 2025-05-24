import logging
import subprocess
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
from .config import DATA_DIR, SECRET_KEY

class FileReader:
    """قراءة الملفات بأنواعها مع دعم متقدم للخطأ وتحسين الأداء"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.supported_formats = ['.doc', '.docx', '.pdf', '.txt', '.odt', '.jpg', '.png', '.jpeg']
        self.cipher = Fernet(SECRET_KEY)
        self.temp_dir = DATA_DIR / "temp"
        self.temp_dir.mkdir(exist_ok=True)

    def read_file(self, file_path: str, encrypt_content: bool = False) -> Optional[str]:
        """قراءة الملف مع معالجة محسنة للأخطاء"""
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"الملف {file_path} غير موجود")
            
            content = self._read_content(file_path)
            return self._process_content(content, encrypt_content)
            
        except Exception as e:
            self.logger.error(f"خطأ في قراءة الملف: {str(e)}", exc_info=True)
            return None

    def _read_content(self, path: str) -> str:
        """التوزيع الداخلي مع دعم تعدد اللغات"""
        file_ext = Path(path).suffix.lower()
        
        if file_ext == '.doc':
            return self._process_legacy_doc(path)
        elif file_ext in ('.jpg', '.png', '.jpeg'):
            return self._extract_image_text(path)
        else:
            return self._extract_standard_text(path)

    def _process_legacy_doc(self, path: str) -> str:
        """معالجة ملفات DOC مع إدارة أفضل للموارد"""
        temp_file = self.temp_dir / "temp.doc"
        try:
            with open(temp_file, 'wb') as f:
                f.write(Path(path).read_bytes())
            
            result = subprocess.run(
                ['antiword', str(temp_file)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"خطأ في معالجة DOC: {e.stderr}")
            return ""
        finally:
            temp_file.unlink(missing_ok=True)

    def _extract_image_text(self, path: str) -> str:
        """استخراج النص من الصور بدعم متعدد اللغات"""
        try:
            from PIL import Image
            import pytesseract
            
            img = Image.open(path)
            return pytesseract.image_to_string(img, lang='ara+eng')
        except ImportError:
            self.logger.error("المكتبات المطلوبة غير مثبتة: Pillow/pytesseract")
            return ""
        except Exception as e:
            self.logger.error(f"خطأ في معالجة الصورة: {str(e)}")
            return ""

    def _extract_standard_text(self, path: str) -> str:
        """استخراج النص من الملفات القياسية"""
        try:
            import textract
            return textract.process(path).decode('utf-8', errors='ignore')
        except textract.exceptions.ExtensionNotSupported:
            self.logger.error("نوع الملف غير مدعوم")
            return ""
        except Exception as e:
            self.logger.error(f"خطأ في استخراج النص: {str(e)}")
            return ""

    def _process_content(self, content: str, encrypt: bool) -> str:
        """معالجة المحتوى النهائي مع التشفير"""
        return self.cipher.encrypt(content.encode()).decode() if encrypt else content