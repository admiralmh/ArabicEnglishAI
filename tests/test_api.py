#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_api.py
==================
اختبارات لوظائف REST API باستخدام `pytest`
"""

import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture
def get_jwt_token():
    """
    تسجيل الدخول للحصول على رمز JWT صالح
    """
    response = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_upload_file(get_jwt_token):
    """
    اختبار تحميل ملف ومعالجته عبر API
    """
    headers = {"Authorization": f"Bearer {get_jwt_token}"}
    files = {"file": ("example.txt", b"هذا ملف اختبار", "text/plain")}
    
    response = requests.post(f"{BASE_URL}/upload/", headers=headers, files=files)
    assert response.status_code == 200
    assert "تم استخراج النص" in response.json()["message"]

def test_analyze_text(get_jwt_token):
    """
    اختبار تحليل النصوص عبر API
    """
    headers = {"Authorization": f"Bearer {get_jwt_token}"}
    payload = {"text": "العدل هو أساس الحكم العادل"}

    response = requests.post(f"{BASE_URL}/analyze/", headers=headers, json=payload)
    assert response.status_code == 200
    assert "sentiment" in response.json()

def test_search_documents(get_jwt_token):
    """
    اختبار البحث في قاعدة البيانات عبر API
    """
    headers = {"Authorization": f"Bearer {get_jwt_token}"}
    params = {"query": "العدل"}

    response = requests.get(f"{BASE_URL}/search/", headers=headers, params=params)
    assert response.status_code == 200
    assert isinstance(response.json()["results"], list)

if __name__ == "__main__":
    pytest.main()