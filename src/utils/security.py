import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

# --------------------------------------------------------------------
# إعداد الإعدادات الأساسية للأمان في التطبيق
# --------------------------------------------------------------------

# المفتاح السري المستخدم لتوقيع وفحص رموز JWT.
# يتم جلبه من متغيرات البيئة إن وُجد، وإلا يُستخدم قيمة افتراضية.
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_here')

# خوارزمية التشفير المستخدمة لتوقيع الـ JWT.
ALGORITHM = "HS256"

# مدة صلاحية رمز الوصول بالدقائق (يمكن تعديلها حسب متطلبات التطبيق).
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# تحديد دليل البيانات الخاص بالمشروع.
# يتم تعيين DATA_DIR بحيث يُشير إلى مجلد "data" في جذر المشروع.
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(current_dir, '..', '..', 'data')

# --------------------------------------------------------------------
# إعداد آلية تشفير كلمات المرور
# --------------------------------------------------------------------

# إنشاء سياق لتشفير كلمات المرور باستخدام bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    التحقق من صحة كلمة المرور المُدخلة مقارنةً بالكلمة المشفرة.
    
    :param plain_password: كلمة المرور النصية.
    :param hashed_password: كلمة المرور بعد التشفير.
    :return: True إذا كانت الكلمتان متطابقتين، وإلا False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    تشفير كلمة المرور المدخلة.
    
    :param password: كلمة المرور النصية.
    :return: الكلمة بعد تشفيرها.
    """
    return pwd_context.hash(password)

# --------------------------------------------------------------------
# وظائف إنشاء وفك تشفير رموز JWT (رموز الوصول)
# --------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    إنشاء رمز وصول JWT يحتوي على البيانات الممررة مع تحديد مدة انتهاء الصلاحية.
    
    :param data: البيانات التي سيتم تضمينها في الرمز (مثل معلومات المستخدم).
    :param expires_delta: فترة زمنية إضافية لانتهاء الصلاحية، إن لم يُحدد يتم استخدام القيمة الافتراضية.
    :return: رمز الدخول المشفر (JWT) كسلسلة نصية.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    فك تشفير رمز الوصول للتحقق من صلاحيته واستخراج البيانات المضمنة به.
    
    :param token: رمز الوصول (JWT) كـ string.
    :return: البيانات المضمنة في الرمز إذا كان صالحاً، أو None في حال وجود خطأ.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None