import textract
import logging
import subprocess
from pathlib import Path
from cryptography.fernet import Fernet
from .config import DATA_DIR, SECRET_KEY

class FileReader:
    """قراءة الملفات بأنواعها مع دعم خاص للملفات القديمة"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['.doc', '.docx', '.pdf', '.txt', '.odt', '.jpg', '.png']
        self.cipher = Fernet(SECRET_KEY.encode())

    def read_file(self, file_path: str, encrypt_content: bool = False) -> str:
        """الدالة الرئيسية لقراءة الملفات مع خيار التشفير"""
        try:
            content = self._read_content(file_path)
            return self.cipher.encrypt(content.encode()).decode() if encrypt_content else content
        except Exception as e:
            self.logger.error(f"فشل قراءة الملف {file_path}: {str(e)}")
            return ""

    def _read_content(self, path: str) -> str:
        """التوزيع الداخلي حسب نوع الملف"""
        file_ext = Path(path).suffix.lower()
        
        if file_ext == '.doc':
            return self._read_old_doc(path)
        elif file_ext in ('.jpg', '.png'):
            return self._read_image(path)
        else:
            return textract.process(path).decode('utf-8', errors='ignore')

    def _read_old_doc(self, path: str) -> str:
        """معالجة ملفات DOC القديمة باستخدام antiword"""
        try:
            temp_path = DATA_DIR / "temp.doc"
            with open(temp_path, 'wb') as f:
                f.write(Path(path).read_bytes())
                
            result = subprocess.run(
                ['antiword', str(temp_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            temp_path.unlink(missing_ok=True)
            return result.stdout
        except Exception as e:
            self.logger.error(f"خطأ في معالجة DOC: {str(e)}")
            return ""

    def _read_image(self, path: str) -> str:
        """استخراج النص من الصور باستخدام pytesseract"""
        try:
            from PIL import Image
            return pytesseract.image_to_string(Image.open(path), lang='ara+eng')
        except Exception as e:
            self.logger.error(f"خطأ في معالجة الصورة: {str(e)}")
            return ""