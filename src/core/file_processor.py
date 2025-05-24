import fitz  # PyMuPDF
from docx import Document
import pytesseract
from PIL import Image
import textract
import re
from typing import List
from camel_tools.morphology.database import MorphologyDB
from camel_tools.disambig.mle import MLEDisambiguator
from pathlib import Path
from loguru import logger

class FileProcessor:
    def __init__(self):
        self.db = MorphologyDB.builtin_db()
        self.disambiguator = MLEDisambiguator(self.db)
        self.stopwords = {'من', 'إلى', 'في', 'على', 'أن'}

    def process_file(self, file_path: str) -> str:
        """استخراج النص من أي تنسيق مدعوم"""
        ext = Path(file_path).suffix.lower()
        try:
            if ext == '.pdf':
                return self._extract_pdf(file_path)
            elif ext == '.docx':
                return self._extract_docx(file_path)
            elif ext in ('.jpg', '.png', '.jpeg'):
                return self._extract_image_text(file_path)
            elif ext == '.txt':
                return self._extract_txt(file_path)
            else:
                raise ValueError(f"التنسيق غير مدعوم: {ext}")
        except Exception as e:
            logger.error(f"خطأ في معالجة الملف: {str(e)}")
            return ""

    def _extract_pdf(self, path: str) -> str:
        """استخراج النص من PDF مع دعم العربية"""
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def _extract_docx(self, path: str) -> str:
        """استخراج النص من DOCX"""
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_image_text(self, path: str) -> str:
        """استخراج النص من الصور"""
        img = Image.open(path)
        return pytesseract.image_to_string(img, lang='ara+eng')

    def _extract_txt(self, path: str) -> str:
        """قراءة ملفات TXT"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def clean_text(self, text: str) -> str:
        """تنظيف النص وإزالة العناصر غير المرغوبة"""
        # إزالة الحركات والأرقام
        cleaned = re.sub(r'[\u064b-\u065f]', '', text)
        cleaned = re.sub(r'\d+', '', cleaned)
        
        # تحليل الجذور
        tokens = self._simple_word_tokenize(cleaned)
        disambig = self.disambiguator.disambiguate(tokens)
        
        # استخراج الجذور المفيدة
        roots = [
            analysis.analyses[0].root
            for analysis in disambig
            if analysis.analyses and analysis.analyses[0].root not in self.stopwords
        ]
        return ' '.join(roots)

    def _simple_word_tokenize(self, text: str) -> List[str]:
        """تفكيك النص إلى كلمات (بديل لـ camel_tools.tokenizers.word.simple_word_tokenize)"""
        return text.split()