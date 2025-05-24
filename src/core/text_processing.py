#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
text_processing.py
==================
معالجة النصوص واستخراج البيانات من مختلف المصادر (PDF، DOCX، DOC، TXT، الصور)
"""

import fitz  # PyMuPDF لقراءة ملفات PDF
import docx
import textract
import pytesseract
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from pathlib import Path
from PIL import Image

class TextProcessor:
    """
    وحدة معالجة النصوص واستخراج البيانات من المستندات والصور
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.supported_formats = {".pdf", ".docx", ".doc", ".txt", ".jpg", ".png"}

    def extract_text(self, file_name: str) -> str:
        """
        استخراج النصوص من ملف داخل المسار المحدد

        :param file_name: اسم الملف داخل مجلد البيانات
        :return: نص مستخرج بعد المعالجة
        """
        file_path = self.data_dir / file_name
        file_ext = file_path.suffix.lower()

        if file_ext not in self.supported_formats:
            raise ValueError(f"تنسيق غير مدعوم: {file_ext}")

        if file_ext == ".pdf":
            return self._extract_from_pdf(file_path)
        elif file_ext in {".docx", ".doc"}:
            return self._extract_from_doc(file_path)
        elif file_ext == ".txt":
            return self._extract_from_txt(file_path)
        elif file_ext in {".jpg", ".png"}:
            return self._extract_from_image(file_path)
        else:
            return ""

    def _extract_from_pdf(self, file_path: Path) -> str:
        """استخراج النصوص من ملف PDF"""
        text = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text.append(page.get_text("text"))
        return "\n".join(text)

    def _extract_from_doc(self, file_path: Path) -> str:
        """استخراج النصوص من ملفات DOCX وDOC باستخدام textract"""
        return textract.process(str(file_path)).decode("utf-8")

    def _extract_from_txt(self, file_path: Path) -> str:
        """استخراج النصوص من ملف TXT"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _extract_from_image(self, file_path: Path) -> str:
        """تحويل الصور إلى نصوص باستخدام OCR"""
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang="ara+eng")
        return self._clean_text(text)

    def _clean_text(self, text: str) -> str:
        """تنظيف النصوص وإعادة تشكيلها باللغة العربية"""
        text = text.strip().replace("\n", " ")
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

# اختبار عملي للكود
if __name__ == "__main__":
    data_dir = Path("C:/Manhal/Manhal ai/data")  # تحديد مسار الملفات
    processor = TextProcessor(data_dir)
    extracted_text = processor.extract_text("example.doc")
    print(extracted_text)