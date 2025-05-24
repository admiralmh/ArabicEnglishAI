#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nlp_analysis.py
==================
تحليل النصوص العربية: الجُمَّل الكبير والصغير، الشعر، والصور البلاغية
"""

import camel_tools.utils.charmap as charmap
import camel_tools.morphology.analyzer as analyzer

class NLPAnalysis:
    """
    وحدة تحليل النصوص لدعم حساب الجُمَّل الكبير والصغير
    """
    def __init__(self):
        self.analyzer = analyzer.Analyzer("calima-msa")

    def calculate_gematria(self, text: str, method="big") -> int:
        """حساب الجُمَّل الكبير والصغير"""
        gematria_map = {"big": {chr(i): i for i in range(1600, 1610)}, "small": {chr(i): i for i in range(1, 10)}}
        return sum(gematria_map[method].get(char, 0) for char in text)

# اختبار عملي
if __name__ == "__main__":
    nlp = NLPAnalysis()
    print(nlp.calculate_gematria("الله", "big"))