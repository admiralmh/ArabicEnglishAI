__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk, filedialog
from core.database import DatabaseManager
from core.file_reader import FileReader

class MainWindow(tk.Tk):
    def __init__(self, db: DatabaseManager, reader: FileReader):
        super().__init__()
        self.db = db
        self.reader = reader
        self.title("منهل - الذكاء الاصطناعي")
        self.geometry("1000x800")
        self._setup_widgets()
    
    def _setup_widgets(self):
        """تهيئة عناصر الواجهة"""
        # إطار تحميل الملفات
        self.file_frame = ttk.LabelFrame(self, text="إدارة الملفات")
        self.file_frame.pack(pady=10, fill=tk.X)
        
        # زر تحميل الملفات
        self.btn_load = ttk.Button(
            self.file_frame,
            text="تحميل ملفات",
            command=self._load_files
        )
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        # منطقة عرض النتائج
        self.result_area = tk.Text(self, wrap=tk.WORD, font=('Arial', 12))
        self.result_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def _load_files(self):
        """معالجة تحميل الملفات"""
        filetypes = (
            ("ملفات نصية", "*.pdf;*.docx;*.txt"),
            ("جميع الملفات", "*.*")
        )
        
        filenames = filedialog.askopenfilenames(
            title="اختر الملفات",
            filetypes=filetypes
        )
        
        if filenames:
            self.result_area.delete(1.0, tk.END)
            for f in filenames:
                content = self.reader.read_file(f)
                self.db.save_document(f.split('/')[-1], content)
                self.result_area.insert(tk.END, f"تم تحميل: {f}\n")

if __name__ == "__main__":
    # للتشغيل الاختباري
    from core.database import DatabaseManager
    from core.file_reader import FileReader
    temp_db = DatabaseManager(":memory:")
    temp_reader = FileReader()
    app = MainWindow(temp_db, temp_reader)
    app.mainloop()