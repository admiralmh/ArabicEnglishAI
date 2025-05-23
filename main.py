from core.file_reader import FileReader
from core.database import DatabaseManager
from gui.windows.main_window import MainWindow
import logging

def configure_logging():
    """تهيئة نظام التسجيل"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('manhal.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """نقطة الدخول الرئيسية للبرنامج"""
    configure_logging()
    
    # تهيئة المكونات الأساسية
    db = DatabaseManager()
    reader = FileReader()
    
    # تشغيل واجهة المستخدم
    app = MainWindow(db, reader)
    app.mainloop()

if __name__ == "__main__":
    main()