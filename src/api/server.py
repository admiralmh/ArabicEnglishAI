#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
server.py
==================
واجهة REST API لمعالجة المستندات والمصادقة باستخدام JWT
"""

import jwt
import uvicorn
import datetime
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path
from ..text_processing import TextProcessor
from ..database import DatabaseManager
from ..ai_engine import AIEngine
from ..config import SECRET_KEY, DATA_DIR

# إعداد FastAPI
app = FastAPI(title="Manhal AI API", version="1.0")

# إعداد المصادقة بـ JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_jwt_token(username: str):
    """
    إنشاء رمز JWT صالح لمدة 24 ساعة
    """
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    """
    التحقق من صحة رمز JWT
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="انتهت صلاحية الرمز")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="رمز غير صالح")

# تهيئة وحدات معالجة النصوص والذكاء الاصطناعي
text_processor = TextProcessor(DATA_DIR)
db = DatabaseManager()
ai_engine = AIEngine()

@app.post("/token", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    تسجيل الدخول وإنشاء رمز JWT
    """
    if form_data.username != "admin" or form_data.password != "password123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="بيانات تسجيل الدخول غير صحيحة")
    
    token = generate_jwt_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/upload/")
def upload_file(file: UploadFile = File(...), username: str = Depends(verify_jwt_token)):
    """
    تحميل ملف ومعالجته واستخراج النصوص منه
    """
    file_path = DATA_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    extracted_text = text_processor.extract_text(file.filename)
    db.save_document(file.filename, extracted_text, Path(file.filename).suffix.upper())
    
    return {"message": f"تم استخراج النص من {file.filename}", "text": extracted_text}

@app.post("/analyze/")
def analyze_text(text: str, username: str = Depends(verify_jwt_token)):
    """
    تحليل النصوص واستخراج المعلومات الذكية
    """
    sentiment = ai_engine.answer_question("ما هو الشعور في هذا النص؟", text)
    return {"sentiment": sentiment}

@app.get("/search/")
def search_documents(query: str, username: str = Depends(verify_jwt_token)):
    """
    البحث عن مستندات داخل قاعدة البيانات
    """
    results = db.search_documents(query)
    return {"results": results}

# تشغيل API محليًا
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)