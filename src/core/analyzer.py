__version__ = "3.0.0"  # إصدار معدّل مع دعم numpy 1.x

import logging
import numpy as np
from camel_tools.morphology.database import MorphologyDB
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator

class ArabicAnalyzer:
    """محلل النصوص العربية مع معالجة مسبقة للتبعيات"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_dependencies()
        self._initialize_models()

    def _check_dependencies(self):
        """التحقق من توافق إصدارات المكتبات"""
        # تحقق من إصدار numpy
        if np.__version__ >= '2.0.0':
            raise ImportError("""
            !خطأ: إصدار numpy غير مدعوم
            - الإصدار المثبت: {}
            - المطلوب: numpy < 2.0.0
            - الحل: pip install numpy==1.26.4
            """.format(np.__version__))
        
        # تحقق من وجود camel-tools
        try:
            import camel_tools
        except ImportError:
            raise ImportError("""
            !خطأ: camel-tools غير مثبت
            - الحل: pip install camel-tools==1.5.6
            """)

    def _initialize_models(self):
        """تهيئة النماذج اللغوية"""
        try:
            self.logger.info("جاري تحميل نماذج معالجة اللغة العربية...")
            self.db = MorphologyDB.builtin_db()
            self.disambiguator = MLEDisambiguator(self.db)
            self.logger.info("تم تحميل النماذج بنجاح")
        except Exception as e:
            self.logger.error(f"فشل تحميل النماذج: {str(e)}")
            raise

    def analyze_text(self, text: str) -> dict:
        """تحليل نص عربي شامل (ترميز، جذور، تصنيف)"""
        analysis = {
            'tokens': [],
            'lemmas': [],
            'roots': [],
            'pos_tags': []
        }
        
        try:
            # المعالجة المسبقة للنص
            cleaned_text = self._preprocess_text(text)
            
            # الترميز والتفكيك
            tokens = simple_word_tokenize(cleaned_text)
            disambig = self.disambiguator.disambiguate(tokens)
            
            # استخراج الميزات
            for word in disambig:
                if word.analyses:
                    best_analysis = word.analyses[0]
                    analysis['tokens'].append(word.word)
                    analysis['lemmas'].append(best_analysis.lemma)
                    analysis['roots'].append(best_analysis.root)
                    analysis['pos_tags'].append(best_analysis.pos)
            
            return analysis
        except Exception as e:
            self.logger.error(f"خطأ في التحليل: {str(e)}")
            return analysis

    def _preprocess_text(self, text: str) -> str:
        """تنظيف النص وإعداده للتحليل"""
        # إزالة الأحرف الخاصة
        cleaned = text.translate(str.maketrans('', '', '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'))
        
        # إزالة الأرقام والحركات
        cleaned = ''.join([c for c in cleaned if not c.isdigit() and not c in 'ًًٌٌٍَُِّ'])
        
        return cleaned.strip()

if __name__ == "__main__":
    # اختبار تشغيلي
    analyzer = ArabicAnalyzer()
    sample_text = "اللغة العربية لغة جميلة وغنية بالمفردات"
    result = analyzer.analyze_text(sample_text)
    print("نتيجة التحليل:", result)