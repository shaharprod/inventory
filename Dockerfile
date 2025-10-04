# Dockerfile למערכת ניהול מלאי
# גרסה: Development (כמו שהיא)

FROM python:3.10-slim

# הגדרת משתני סביבה
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# יצירת ספריית עבודה
WORKDIR /app

# התקנת תלויות מערכת
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# העתקת requirements
COPY requirements.txt .

# התקנת תלויות Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# העתקת כל הקוד
COPY . .

# יצירת ספריות נדרשות
RUN mkdir -p logs backups media/products media/barcodes

# הרצת migrations והפעלת שרת
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
