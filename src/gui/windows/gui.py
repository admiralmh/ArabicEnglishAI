import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import os

class GUI:
    def __init__(self, root, db, reader, detector, translator, analyzer, ai):
        self.root = root
        self.db = db
        self.reader = reader
        self.detector = detector
        self.translator = translator
        self.analyzer = analyzer
        self.ai = ai

        self.root.title("منهل - الذكاء الاصطناعي")

        self.label = tk.Label(root, text="تحميل ملفات:")
        self.label.pack()

        self.load_btn = tk.Button(root, text="اختر ملفات", command=self.load_files)
        self.load_btn.pack()

        self.preview = scrolledtext.ScrolledText(root, height=15)
        self.preview.pack(fill=tk.BOTH, expand=True)

        self.class_label = tk.Label(root, text="تصنيف الملف:")
        self.class_label.pack()
        self.class_entry = tk.Entry(root)
        self.class_entry.pack()

        self.analyze_btn = tk.Button(root, text="تحليل النص", command=self.analyze_text)
        self.analyze_btn.pack()

        self.q_entry = tk.Entry(root, width=80)
        self.q_entry.pack()
        self.a_box = scrolledtext.ScrolledText(root, height=5)
        self.a_box.pack(fill=tk.BOTH, expand=True)

        self.ask_btn = tk.Button(root, text="اسأل", command=self.ask_question)
        self.ask_btn.pack()

        self.files = []
        self.current_text = ""

    def load_files(self):
        paths = filedialog.askopenfilenames()
        self.files = paths
        content = ""
        for path in paths:
            content += f"--- {os.path.basename(path)} ---\n"
            content += self.reader.read_file(path)
            content += "\n\n"
        self.current_text = content
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, content)

    def analyze_text(self):
        if not self.current_text:
            messagebox.showwarning("تحذير", "لم يتم تحميل أي ملف")
            return
        summary = self.analyzer.summarize(self.current_text)
        sentiment = self.analyzer.sentiment(self.current_text)
        classification = self.class_entry.get() or "غير مصنف"
        for path in self.files:
            self.db.save_file_classification(os.path.basename(path), classification)
        self.preview.insert(tk.END, f"\n\n[الملخص]: {summary}\n[المشاعر]: {sentiment}")

    def ask_question(self):
        question = self.q_entry.get()
        if not question or not self.current_text:
            return
        answer = self.ai.answer_question(question, self.current_text)
        self.a_box.delete(1.0, tk.END)
        self.a_box.insert(tk.END, answer)
        self.db.save_qa_pair("admin", question, answer)