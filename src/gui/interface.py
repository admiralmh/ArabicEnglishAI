#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
interface.py
==================
واجهة المستخدم الرسومية لإدارة المستندات وتحليل النصوص
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QFileDialog, QVBoxLayout, QWidget
from ..core.text_processing import TextProcessor
from ..core.database import DatabaseManager
from ..core.ai_engine import AIEngine
from ..config import DATA_DIR

class AIInterface(QMainWindow):
    """
    واجهة المستخدم الرسومية للتحكم في معالجة النصوص وتحليلها
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manhal AI - معالجة النصوص")
        self.setGeometry(200, 200, 900, 600)

        # تهيئة وحدات المعالجة
        self.text_processor = TextProcessor(DATA_DIR)
        self.db = DatabaseManager()
        self.ai_engine = AIEngine()

        # إنشاء عناصر الواجهة
        self.init_ui()

    def init_ui(self):
        """
        تهيئة عناصر واجهة المستخدم
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("اختر ملفًا لمعالجته:")
        layout.addWidget(self.label)

        self.upload_button = QPushButton("تحميل ملف")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.result_area = QTextEdit()
        self.result_area.setPlaceholderText("سيظهر النص المستخرج والمعالج هنا...")
        layout.addWidget(self.result_area)

        self.analyze_button = QPushButton("تحليل النص")
        self.analyze_button.clicked.connect(self.analyze_text)
        layout.addWidget(self.analyze_button)

        self.search_button = QPushButton("بحث عن المستندات")
        self.search_button.clicked.connect(self.search_documents)
        layout.addWidget(self.search_button)

        central_widget.setLayout(layout)

    def upload_file(self):
        """
        تحميل ملف واستخراج النص منه
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملفًا", "", "Documents (*.pdf *.docx *.doc *.txt *.jpg *.png)")
        if file_path:
            extracted_text = self.text_processor.extract_text(Path(file_path).name)
            self.db.save_document(Path(file_path).name, extracted_text, Path(file_path).suffix.upper())
            self.result_area.setText(extracted_text)

    def analyze_text(self):
        """
        تشغيل التحليل الذكي للنصوص وعرض النتائج
        """
        text = self.result_area.toPlainText()
        if not text.strip():
            self.result_area.setText("الرجاء تحميل ملف أولًا.")
            return

        sentiment = self.ai_engine.answer_question("ما هو الشعور في هذا النص؟", text)
        poetry_meter = self.ai_engine.answer_question("ما هو بحر هذا الشعر؟", text)
        self.result_area.append(f"\n🔹 تحليل المشاعر: {sentiment}")
        self.result_area.append(f"\n🔹 بحر الشعر المتوقع: {poetry_meter}")

    def search_documents(self):
        """
        البحث داخل قاعدة البيانات وعرض النتائج
        """
        query, _ = QFileDialog.getOpenFileName(self, "إدخال كلمة للبحث", "")
        results = self.db.search_documents(query)
        if results:
            self.result_area.setText("🔍 نتائج البحث:\n" + "\n".join([f"{doc['id']}: {doc['title']}" for doc in results]))
        else:
            self.result_area.setText("❌ لم يتم العثور على مستندات مطابقة.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIInterface()
    window.show()
    sys.exit(app.exec())