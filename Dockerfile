# שלב 1: תמונת בסיס - Python 3.10
FROM python:3.10-slim

# הגדרת משתני סביבה
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=inventory_project.settings \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# התקנת תלויות מערכת
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libffi-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# יצירת משתמש לא-root לאבטחה
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/media /app/logs /app/backups && \
    chown -R appuser:appuser /app

# הגדרת תיקיית עבודה
WORKDIR /app

# העתקת requirements והתקנת חבילות Python
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# העתקת כל הקבצים
COPY --chown=appuser:appuser . .

# יצירת תיקיות נדרשות
RUN mkdir -p media/products media/barcodes logs backups static staticfiles && \
    chown -R appuser:appuser media logs backups static staticfiles

# מעבר למשתמש לא-root
USER appuser

# חשיפת פורט
EXPOSE 8000

# הרצת collectstatic, migrations ושרת
CMD ["sh", "-c", "\
    python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000\
"]
