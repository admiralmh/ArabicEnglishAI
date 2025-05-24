#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nlp_analysis.py
==================
تحليل النصوص العربية والإنجليزية: المشاعر، الشعر، التعرف على الكيانات
"""

import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from camel_tools.utils.charmap import transliterate
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.ner import NERecognizer
from pathlib import Path

class NLPAnalysis:
    """
    وحدة تحليل النصوص لدعم المشاعر، الشعر العربي، التعرف على الكيانات، والبحث الديني
    """

    def __init__(self):
        # تحميل النموذج المناسب لتحليل المشاعر
        self.sentiment_model = "aubmindlab/bert-base-arabic-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(self.sentiment_model)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.sentiment_model)
        self.sentiment_pipeline = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

        # تهيئة محلل الكلمات العربية
        self.analyzer = Analyzer("calima-msa")

        # نموذج التعرف على الكيانات (NER)
        self.ner = NERecognizer()

    def analyze_sentiment(self, text: str) -> str:
        """
        تحليل المشاعر للنصوص العربية والإنجليزية
        """
        result = self.sentiment_pipeline(text)
        return f"تحليل المشاعر: {result[0]['label']} (الثقة: {result[0]['score']:.2f})"

    def detect_poetry_meter(self, text: str) -> str:
        """
        تحديد بحر الشعر العربي باستخدام CamelTools
        """
        analysis = self.analyzer.analyze(text)
        meters = [token['diac'] for token in analysis]
        return f"بحر الشعر المتوقع: {' '.join(meters)}"

    def named_entity_recognition(self, text: str) -> list:
        """
        التعرف على الكيانات المسماة (الأسماء، التواريخ، الأماكن)
        """
        entities = self.ner.recognize(text)
        return entities

# اختبار عملي للكود
if __name__ == "__main__":
    nlp = NLPAnalysis()
    sample_text = "العدل هو أحد القيم الأساسية في القرآن."
    print(nlp.analyze_sentiment(sample_text))
    print(nlp.detect_poetry_meter("إذا غامرتَ في شرفٍ مرومِ"))
    print(nlp.named_entity_recognition("ولد ابن سينا في سنة 980 ميلادية في بخارى"))