import tkinter as tk
from tkinter import ttk, filedialog
from ..core.file_processor import FileProcessor
from .widgets.progress_bar import CustomProgressBar

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("منهل AI - معالج النصوص الذكي")
        self.geometry("1200x800")
        self.file_processor = FileProcessor()
        self.progress_bar = CustomProgressBar(self)
        self._setup_ui()

    def _setup_ui(self):
        # شريط الأدوات
        toolbar = ttk.Frame(self)
        btn_load = ttk.Button(toolbar, text="تحميل ملف", command=self.load_file)
        btn_load.pack(side=tk.LEFT, padx=5)
        toolbar.pack(fill=tk.X)

        # منطقة النتائج
        self.text_area = tk.Text(self, wrap=tk.WORD, font=('Arial', 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

    def load_file(self):
        """معالجة الملفات المحددة"""
        files = filedialog.askopenfilenames(filetypes=[("ملفات مدعومة", SUPPORTED_FORMATS)])
        for file in files:
            self.progress_bar.start()
            content = self.file_processor.process_file(file)
            self.text_area.insert(tk.END, content + "\n\n")
            self.progress_bar.complete()