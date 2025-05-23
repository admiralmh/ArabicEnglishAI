import database

class SelfLearning:
    def __init__(self):
        self.known_fixes = {}  # مفتاح: سؤال، قيمة: تصحيح الإجابة

    def add_correction(self, question, correct_answer):
        self.known_fixes[question] = correct_answer

    def correct_answer(self, question, current_answer):
        if question in self.known_fixes:
            return self.known_fixes[question]
        return current_answer

    def save_corrections_to_db(self):
        # إذا أردت حفظ التصحيحات في قاعدة بيانات أو ملف، ضع هنا المنطق
        pass

# مثلاً للاستخدام في النموذج:
self_learning = SelfLearning()
