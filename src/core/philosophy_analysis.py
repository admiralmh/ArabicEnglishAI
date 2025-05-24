#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
philosophy_analysis.py
==================
تحليل النصوص الفلسفية واستخراج الحجج والربط بين الفلسفة والعلوم
"""

from transformers import pipeline
import camel_tools.utils.charmap as charmap

class PhilosophyAnalysis:
    """
    وحدة تحليل النصوص الفلسفية واستخراج الأفكار والمفاهيم المجردة
    """
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="aubmindlab/bert-base-arabic-sentiment")

    def analyze_philosophical_text(self, text: str) -> str:
        """تحليل الأفكار الفلسفية واستخراج الحجج النقدية"""
        reshaped_text = charmap.transliterate(text)
        sentiment = self.sentiment_pipeline(text)
        return f"تحليل الفلسفة: {reshaped_text}\n🔹 الشعور العام: {sentiment[0]['label']}"

# اختبار عملي
if __name__ == "__main__":
    pa = PhilosophyAnalysis()
    print(pa.analyze_philosophical_text("ما هو معنى الوعي؟"))