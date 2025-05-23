__version__ = "1.1.0"  # دعم استيراد صحيح

import tkinter as tk
from tkinter import ttk, filedialog
from core.database import DatabaseManager
from core.file_reader import FileReader

class MainWindow(tk.Tk):
    def __init__(self, db: DatabaseManager, reader: FileReader):
        super().__init__()
        self.db = db
        self.reader = reader
        self._setup_ui()
        
    def _setup_ui(self):
        """تهيئة عناصر الواجهة"""
        self.title("منهل - الذكاء الاصطناعي")
        self.geometry("1000x800")
        
        # عناصر التحكم
        self.file_frame = ttk.LabelFrame(self, text="إدارة الملفات")
        self.file_frame.pack(pady=10, fill=tk.X)
        
        self.btn_load = ttk.Button(
            self.file_frame,
            text="تحميل ملفات",
            command=self.load_files
        )
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        # منطقة النتائج
        self.result_area = tk.Text(self, wrap=tk.WORD, font=('Arial', 12))
        self.result_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
    def load_files(self):
        """تحميل الملفات المحددة"""
        filetypes = (
            ("ملفات المدعومة", "*.pdf;*.docx;*.txt;*.doc"),
            ("جميع الملفات", "*.*")
        )
        
        filenames = filedialog.askopenfilenames(
            title="اختر الملفات",
            filetypes=filetypes
        )
        
        if filenames:
            for f in filenames:
                content = self.reader.read_file(f)
                self.db.save_document(f.split('/')[-1], content)
                self.result_area.insert(tk.END, f"تم تحميل: {f}\n")

if __name__ == "__main__":
    # للتشغيل الاختباري
    temp_db = DatabaseManager(":memory:")
    temp_reader = FileReader()
    app = MainWindow(temp_db, temp_reader)
    app.mainloop()