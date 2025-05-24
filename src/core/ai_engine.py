"""
File: C:\Manhal\Manhal ai\src\core\ai_engine.py

الوصف:
تجمع هذه الوحدة بين وظائف استخراج النصوص من أنواع الملفات المختلفة (صور، PDF، DOCX، TXT)
ومعالجتها باستخدام الذكاء الاصطناعي. يشمل ذلك تشغيل تقنيات OCR والتعامل مع ملفات PDF 
باستخدام PyMuPDF، وأيضاً استخراج وتحليل البيانات نصيةً عبر إحدى وحدات المعالجة المخصصة (TextProcessor)، 
كما يقوم بتخزين نتائج التحليل بقاعدة البيانات عبر DatabaseManager.
"""

import os
import torch
import pytesseract
import textract
import fitz  # PyMuPDF لقراءة ملفات PDF

# استخدام استيراد مسار مطلق للوحدات الداخلية
from core.text_processing import TextProcessor
from core.database import DatabaseManager
from utils.security import SECRET_KEY, DATA_DIR


class AIEngine:
    """
    توفر هذه الفئة الوظائف التالية:
      - استخراج النصوص من الصور باستخدام OCR.
      - قراءة الملفات بصيغة PDF وDOCX.
      - تحليل النصوص باستخدام وحدة TextProcessor.
      - حفظ نتائج التحليل في قاعدة البيانات.
    """

    def __init__(self):
        self.text_processor = TextProcessor()
        self.database_manager = DatabaseManager()
        self.ocr_engine = pytesseract  # استخدام pytesseract لاستخراج النصوص من الصور
        self.pdf_engine = fitz         # استخدام PyMuPDF لقراءة ملفات PDF

    def extract_text_from_image(self, image_path: str) -> str:
        """
        استخراج النصوص من صورة بواسطة تقنية OCR.
        :param image_path: مسار ملف الصورة.
        :return: النص المستخرج من الصورة.
        """
        return self.ocr_engine.image_to_string(image_path)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        استخراج النصوص من ملف PDF باستخدام PyMuPDF.
        :param pdf_path: مسار ملف PDF.
        :return: النص المستخرج من الملف.
        """
        doc = self.pdf_engine.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def extract_text_from_docx(self, docx_path: str) -> str:
        """
        استخراج النصوص من ملف DOCX باستخدام مكتبة textract.
        :param docx_path: مسار ملف DOCX.
        :return: النص المستخرج من الملف.
        """
        # textract تُرجع نصاً مُشفرًا بالبايت، لذا نقوم بفك التشفير
        return textract.process(docx_path).decode("utf-8")

    def analyze_text(self, text: str) -> dict:
        """
        يقوم بتحليل النص عبر دوال معالجة النصوص من وحدة TextProcessor.
        :param text: النص المُدخل للتحليل.
        :return: قاموس يحتوي على نتائج التحليل (تنظيف النص، استخراج الكيانات، الكشف عن اللغة، تحليل المشاعر، الحساب العددي، التلخيص، والكلمات المفتاحية).
        """
        analysis = {
            "cleaned_text": self.text_processor.clean_text(text),
            "entities": self.text_processor.extract_entities(text),
            "language": self.text_processor.detect_language(text),
            "sentiment": self.text_processor.analyze_sentiment(text),
            "numerical_analysis": self.text_processor.numerical_analysis(text),
            "summary": self.text_processor.summarize_text(text),
            "keywords": self.text_processor.extract_keywords(text)
        }
        return analysis

    def save_analysis_results(self, analysis_data: dict):
        """
        حفظ نتائج التحليل إلى قاعدة البيانات باستخدام وحدة DatabaseManager.
        :param analysis_data: البيانات التحليلية المُجمعة.
        """
        self.database_manager.save_data("analysis_results", analysis_data)

    def run_engine(self, input_path: str) -> dict:
        """
        تشغيل محرك الذكاء الاصطناعي على ملف الإدخال المحدد (صورة، PDF، DOCX أو TXT).
        يتم تحديد نوع الملف بناءً على الامتداد واستخراج النص وفقاً لذلك، ثم تحليل النص وحفظ النتائج.
        :param input_path: مسار ملف الإدخال.
        :return: قاموس يحتوي على نتائج التحليل.
        """
        ext = os.path.splitext(input_path)[1].lower()
        if ext in [".png", ".jpg", ".jpeg"]:
            text = self.extract_text_from_image(input_path)
        elif ext == ".pdf":
            text = self.extract_text_from_pdf(input_path)
        elif ext in [".docx", ".doc"]:
            text = self.extract_text_from_docx(input_path)
        elif ext == ".txt":
            with open(input_path, encoding="utf-8") as f:
                text = f.read()
        else:
            raise ValueError("تنسيق الملف غير مدعوم")
        
        analysis = self.analyze_text(text)
        self.save_analysis_results(analysis)
        return analysis