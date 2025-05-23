# نموذج بسيط لترجمة باستخدام مكتبة googletrans
from googletrans import Translator as GoogleTranslator

class Translator:
    def __init__(self):
        self.translator = GoogleTranslator()

    def translate(self, text, src='auto', dest='ar'):
        try:
            result = self.translator.translate(text, src=src, dest=dest)
            return result.text
        except Exception as e:
            return f"خطأ في الترجمة: {e}"
