__version__ = "1.1.0"  # إضافة دالة main واضحة

from core.database import DatabaseManager
from core.file_reader import FileReader
from gui.windows.main_window import MainWindow
import logging

def main():
    """الدالة الرئيسية لتشغيل البرنامج"""
    try:
        # تهيئة النظام
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # إنشاء الكائنات الأساسية
        db = DatabaseManager()
        reader = FileReader()
        
        # تشغيل الواجهة
        app = MainWindow(db, reader)
        app.mainloop()
        
    except Exception as e:
        logging.critical(f"فشل التشغيل: {str(e)}")
        raise

if __name__ == "__main__":
    main()