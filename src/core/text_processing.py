"""
File: C:\Manhal\Manhal ai\src\core\text_processing.py

الغرض:
- معالجة النصوص الواردة من الملفات (DOCX, PDF, TXT) واستخراج محتوياتها.
- تنظيف النصوص وإزالة الكلمات غير المهمة لتحسين التحليل.
- استخراج الكيانات الأساسية مثل الأسماء، التواريخ والأماكن.
- الكشف عن لغة النص (عربي/إنجليزي).
- دعم الترجمة الذكية بين اللغات (باستخدام Google Translate إن وجد).
- تحليل المشاعر بطريقة مبسطة.
- إجراء التحليل العددي للأحرف العربية (نظام الجُمَّل).
- تلخيص النصوص واستخراج الكلمات المفتاحية.

يمكن استخدام هذا الموديل كأساس لتطوير برنامج ذكاء اصطناعي يقوم بفهم وإستنتاج الإجابات من الملفات النصية وتنفيذ مزيد من التحليلات المتقدمة مثل تحليل النصوص الدينية والأدبية.
"""

import re
import string

# محاولة استيراد مترجم googletrans لتعزيز الترجمة الذكية
try:
    from googletrans import Translator
    translator_available = True
except ImportError:
    translator_available = False


class TextProcessor:
    """
    وحدة معالجة النصوص لتحليل وتجميع المعلومات من الملفات.
    
    تتضمن الوظائف:
      - تنظيف النصوص وإزالة علامات الترقيم والكلمات الزائدة.
      - استخراج الكيانات (تواريخ، أسماء، أماكن) باستخدام تعابير نمطية.
      - كشف لغة النص (عربي أو إنجليزي).
      - ترجمة النصوص بين اللغات (إن توافرت مكتبة googletrans).
      - تحليل المشاعر باستخدام أسلوب مبسط.
      - الحساب العددي للأحرف العربية باستخدام نظام الجُمَّل.
      - تلخيص النص واستخراج الكلمات المفتاحية.
      - معالجة شاملة للنص تجمع نتائج التحليل المختلفة.
    """

    def __init__(self):
        if translator_available:
            self.translator = Translator()

    def clean_text(self, text: str) -> str:
        """
        تنظيف النص بإزالة علامات الترقيم والفارغات الزائدة وتحويله إلى صيغة موحدة.
        """
        cleaned_text = text.strip()
        # إزالة علامات الترقيم
        translator_table = str.maketrans('', '', string.punctuation)
        cleaned_text = cleaned_text.translate(translator_table)
        # تحويل النص إلى أحرف صغيرة (يساهم في تحسين التحليل للغة الإنجليزية)
        cleaned_text = cleaned_text.lower()
        return cleaned_text

    def extract_entities(self, text: str) -> dict:
        """
        استخراج الكيانات الأساسية مثل التواريخ والأسماء والأماكن.
        يعتمد هذا الأسلوب على تعابير نمطية بسيطة.
        """
        entities = {
            "dates": [],
            "names": [],
            "places": []
        }
        # استخراج التواريخ بصيغ مثل dd/mm/yyyy أو dd-mm-yyyy
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        entities["dates"] = dates

        # استخراج الأسماء باللغة الإنجليزية (كلمات تبدأ بحرف كبير)
        names = re.findall(r'\b[A-Z][a-z]+\b', text)
        entities["names"] = list(set(names))

        # استخراج الأماكن: يمكن تطوير هذه الوظيفة باستخدام مكتبات NER في المستقبل
        entities["places"] = []
        return entities

    def detect_language(self, text: str) -> str:
        """
        الكشف عن لغة النص؛ إذا وجد حروف عربية فإن اللغة تكون "ar"، وإلا "en".
        """
        if re.search(r'[\u0600-\u06FF]', text):
            return "ar"
        return "en"

    def translate_text(self, text: str, dest_language: str) -> str:
        """
        ترجمة النص إلى اللغة المستهدفة باستخدام مكتبة googletrans.
        """
        if translator_available:
            try:
                result = self.translator.translate(text, dest=dest_language)
                return result.text
            except Exception as e:
                return f"Translation error: {e}"
        else:
            return "Translation module not available"

    def analyze_sentiment(self, text: str) -> dict:
        """
        تحليل المشاعر باستخدام أسلوب مبسط يعتمد على عد الكلمات الإيجابية والسلبية.
        """
        positive_words = ['good', 'great', 'excellent', 'happy', 'positive', 'جميل', 'سعيد']
        negative_words = ['bad', 'sad', 'poor', 'negative', 'terrible', 'سيء', 'حزين']
        text_lower = text.lower()
        pos_count = sum(text_lower.count(word) for word in positive_words)
        neg_count = sum(text_lower.count(word) for word in negative_words)
        overall = "neutral"
        if pos_count > neg_count:
            overall = "positive"
        elif neg_count > pos_count:
            overall = "negative"
        return {"positive": pos_count, "negative": neg_count, "overall": overall}

    def numerical_analysis(self, text: str) -> dict:
        """
        إجراء حساب عددي للأحرف العربية باستخدام نظام الجُمَّل.
        """
        # تعريف قيم الحروف العربية وفق نظام الجُمَّل
        abjad_values = {
            'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5,
            'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ي': 10, 'ك': 20, 'ل': 30,
            'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100,
            'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800,
            'ظ': 900, 'غ': 1000
        }
        # استخراج الأحرف العربية من النص
        arabic_letters = re.findall(r'[\u0621-\u064A]', text)
        total_value = sum(abjad_values.get(letter, 0) for letter in arabic_letters)
        return {"arabic_letter_sum": total_value, "arabic_letter_count": len(arabic_letters)}

    def summarize_text(self, text: str) -> str:
        """
        تلخيص النص بشكل مبسط باختيار الجمل الأولى.
        """
        sentences = re.split(r'(?<=[.!؟])\s+', text.strip())
        if len(sentences) > 2:
            return ' '.join(sentences[:2])
        return text

    def extract_keywords(self, text: str) -> list:
        """
        استخراج الكلمات المفتاحية من النص بعد إزالة الكلمات الشائعة.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        # قائمة كلمات شائعة باللغتين الإنجليزية والعربية
        stopwords = set([
            "the", "and", "is", "in", "on", "at", "a", "an",
            "من", "في", "على", "ال", "و", "كما", "عن", "ما", "إلى"
        ])
        filtered_words = [word for word in words if word not in stopwords and len(word) > 3]
        frequency = {}
        for word in filtered_words:
            frequency[word] = frequency.get(word, 0) + 1
        sorted_keywords = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, count in sorted_keywords[:5]]
        return top_keywords

    def process_text(self, text: str) -> dict:
        """
        عملية شاملة لمعالجة النصوص تشمل:
         - تنظيف النص.
         - استخراج الكيانات.
         - الكشف عن اللغة.
         - تحليل المشاعر.
         - الحساب العددي للأحرف.
         - تلخيص النص.
         - استخراج الكلمات المفتاحية.
        
        تُرجع هذه الدالة نتيجة شاملة في شكل قاموس.
        """
        cleaned = self.clean_text(text)
        entities = self.extract_entities(text)
        language = self.detect_language(text)
        sentiment = self.analyze_sentiment(text)
        numerical = self.numerical_analysis(text)
        summary = self.summarize_text(text)
        keywords = self.extract_keywords(text)
        return {
            "cleaned_text": cleaned,
            "entities": entities,
            "language": language,
            "sentiment": sentiment,
            "numerical_analysis": numerical,
            "summary": summary,
            "keywords": keywords
        }