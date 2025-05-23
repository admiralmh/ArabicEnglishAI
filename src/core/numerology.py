class NumerologyCalculator:
    def __init__(self):
        self.jummal_values = {
            'أ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 
            'ح': 8, 'ط': 9, 'ي': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50,
            'س': 60, 'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200, 
            'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800,
            'ظ': 900, 'غ': 1000
        }
    
    def calculate_jummal(self, text: str) -> int:
        """حساب قيمة الجُمَّل الكبير للنص العربي"""
        total = 0
        cleaned_text = self._clean_arabic_text(text)
        
        for char in cleaned_text:
            total += self.jummal_values.get(char, 0)
        
        return total
    
    def _clean_arabic_text(self, text: str) -> str:
        """تنظيف النص من التشكيل والأحغير العربية"""
        return ''.join([c for c in text if c in self.jummal_values])