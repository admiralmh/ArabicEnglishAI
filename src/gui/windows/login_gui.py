import tkinter as tk
from tkinter import messagebox
from security import Security

class LoginGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.security = Security()

        self.root.title("تسجيل الدخول")

        tk.Label(root, text="اسم المستخدم:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="كلمة المرور:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_btn = tk.Button(root, text="دخول", command=self.login)
        self.login_btn.pack()

        self.register_btn = tk.Button(root, text="مستخدم جديد", command=self.register)
        self.register_btn.pack()

        self.authenticated_user = None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        stored_hash = self.db.get_user_password(username)
        if stored_hash and self.security.verify_password(password, stored_hash):
            self.authenticated_user = username
            self.root.destroy()
        else:
            messagebox.showerror("خطأ", "بيانات الدخول غير صحيحة")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.get_user_password(username):
            messagebox.showerror("خطأ", "اسم المستخدم موجود بالفعل")
        else:
            hashed = self.security.hash_password(password)
            self.db.add_user(username, hashed)
            messagebox.showinfo("نجاح", "تم تسجيل المستخدم بنجاح")
