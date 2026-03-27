# استخدم صورة Python رسمية
FROM python:3.12-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع
COPY requirements.txt .
COPY app ./app
COPY templates ./templates
COPY static ./static

# تثبيت المتطلبات
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# تعيين الأمر الافتراضي لتشغيل FastAPI باستخدام Uvicorn
# --host 0.0.0.0 يسمح بالوصول من خارج الحاوية
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
