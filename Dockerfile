# מערכת ניהול מלאי - Docker
FROM python:3.11-slim

# הגדרת משתני סביבה
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# עדכון מערכת והתקנת חבילות נדרשות
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    && rm -rf /var/lib/apt/lists/*

# יצירת תיקיית עבודה
WORKDIR /app

# העתקת קבצי requirements
COPY requirements.txt .

# התקנת חבילות Python
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד האפליקציה
COPY . .

# יצירת תיקיות נדרשות
RUN mkdir -p media/products media/barcodes backups static

# הגדרת הרשאות
RUN chmod -R 755 media backups static

# יצירת משתמש לא-root
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# חשיפת פורט
EXPOSE 8000

# פקודת הפעלה
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "inventory_project.wsgi:application"]
