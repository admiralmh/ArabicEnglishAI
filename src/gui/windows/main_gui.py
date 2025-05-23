# main_gui.py

import tkinter as tk
from tkinter import messagebox
from language_detector import LanguageDetector

class ManhalAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manhal AI")

        self.detector = LanguageDetector()

        self.text_input = tk.Text(root, height=10, width=60)
        self.text_input.pack(pady=10)

        self.detect_button = tk.Button(root, text="اكتشاف اللغة", command=self.detect_language)
        self.detect_button.pack()

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def detect_language(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("تحذير", "الرجاء إدخال نص لاكتشاف اللغة.")
            return

        try:
            lang, confidence = self.detector.detect(text)
            if lang:
                self.result_label.config(
                    text=f"اللغة المكتشفة: {lang} (الدقة: {confidence:.2f})"
                )
            else:
                self.result_label.config(text="تعذر اكتشاف اللغة.")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء اكتشاف اللغة:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ManhalAIApp(root)
    root.mainloop()
