#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ai_engine.py
==================
نظام الذكاء الاصطناعي لاستنتاج الإجابات وتحليل الأسئلة
"""

import torch
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from pathlib import Path
from ..text_processing import TextProcessor
from ..database import DatabaseManager
from ..config import DATA_DIR
from deep_translator import GoogleTranslator

class AIEngine:
    """
    وحدة الذكاء الاصطناعي لفهم الأسئلة والبحث عن إجابات ذكية داخل البيانات
    """

    def __init__(self):
        # تحميل نموذج الإجابة الذكية
        self.model_name = "deepset/bert-base-cased-squad2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        self.qa_pipeline = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)

        # تهيئة وحدات معالجة النصوص وقاعدة البيانات
        self.text_processor = TextProcessor(DATA_DIR)
        self.db = DatabaseManager()

    def answer_question(self, question: str, context: str) -> str:
        """
        استنتاج الإجابة بناءً على سياق النص المخزن في قاعدة البيانات
        """
        result = self.qa_pipeline(question=question, context=context)
        return f"الإجابة: {result['answer']} (الثقة: {result['score']:.2f})"

    def search_answer(self, question: str) -> str:
        """
        البحث عن إجابة داخل قاعدة البيانات باستخدام تحليل ذكي
        """
        documents = self.db.search_documents(question)
        if not documents:
            return "لم يتم العثور على إجابة مناسبة."

        # استخدام أول مستند مطابق كمرجع للإجابة
        doc_content = self.db.get_document(documents[0]["id"])["content"]
        return self.answer_question(question, doc_content)

    def translate_text(self, text: str, target_lang: str = "en") -> str:
        """
        ترجمة الإجابات بين العربية والإنجليزية مع الحفاظ على السياق
        """
        return GoogleTranslator(source="auto", target=target_lang).translate(text)

# اختبار عملي للكود
if __name__ == "__main__":
    ai_engine = AIEngine()
    sample_question = "ما هي القيم الأساسية في القرآن؟"
    print(ai_engine.search_answer(sample_question))
    print(ai_engine.translate_text("العدل هو أحد المبادئ المهمة في الإسلام", "en"))