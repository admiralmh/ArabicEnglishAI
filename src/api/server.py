#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
server.py
==================
تحسين REST API عبر FastAPI مع دعم المصادقة بـ JWT وتحليل النصوص الذكية
"""

import jwt
import uvicorn
import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path
from core.text_processing import TextProcessor
from core.database import DatabaseManager
from core.ai_engine import AIEngine
from core.security import SecurityManager
from config import SECRET_KEY, DATA_DIR

app = FastAPI(title="Manhal AI API", version="2.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_jwt_token(username: str):
    """إنشاء رمز JWT صالح لمدة 24 ساعة"""
    payload = {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    """التحقق من صحة رمز JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="انتهت صلاحية الرمز")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="رمز غير صالح")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """تسجيل الدخول وإنشاء رمز JWT"""
    if form_data.username != "admin" or form_data.password != "password123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="بيانات تسجيل الدخول غير صحيحة")
    return {"access_token": generate_jwt_token(form_data.username), "token_type": "bearer"}

@app.post("/upload/")
def upload_file(file: UploadFile = File(...), username: str = Depends(verify_jwt_token)):
    """تحميل ملف واستخراج النصوص منه"""
    file_path = DATA_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    extracted_text = TextProcessor(DATA_DIR).extract_text(file.filename)
    DatabaseManager().save_document(file.filename, extracted_text, Path(file.filename).suffix.upper())
    return {"message": f"تم استخراج النص من {file.filename}", "text": extracted_text}

@app.post("/analyze/")
def analyze_text(text: str, username: str = Depends(verify_jwt_token)):
    """تحليل النصوص واستخراج المعلومات الذكية"""
    sentiment = AIEngine().answer_question("ما هو الشعور في هذا النص؟", text)
    return {"sentiment": sentiment}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)