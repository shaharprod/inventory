# 🔧 תיעוד טכני למפתחים

## 📋 תוכן עניינים

1. [ארכיטקטורה](#ארכיטקטורה)
2. [מודלים](#מודלים)
3. [Views](#views)
4. [פקודות ניהול](#פקודות-ניהול)
5. [API פנימי](#api-פנימי)
6. [הרחבות עתידיות](#הרחבות-עתידיות)

---

## 🏗️ ארכיטקטורה

### מבנה כללי:
```
Django MVT (Model-View-Template) Architecture

┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│   URLs      │  ← Routing
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Views     │  ← Business Logic
└──────┬──────┘
       │
       ├──────► Models (Database)
       │
       └──────► Templates (HTML)
```

### טכנולוגיות:
- **Backend:** Django 5.2, Python 3.10+
- **Database:** SQLite (ניתן לשדרג ל-PostgreSQL/MySQL)
- **Frontend:** Bootstrap 5, Font Awesome, Chart.js
- **PDF:** ReportLab
- **Images:** Pillow

---

## 📊 מודלים (Models)

### Product (מוצר)
```python
class Product(models.Model):
    name = CharField(max_length=200)
    sku = CharField(max_length=50, unique=True)
    barcode = CharField(max_length=100, unique=True, blank=True)
    category = ForeignKey(Category)
    supplier = ForeignKey(Supplier)
    quantity = PositiveIntegerField(default=0)
    location = ForeignKey(Location)
    price = DecimalField(max_digits=10, decimal_places=2)
    cost = DecimalField(max_digits=10, decimal_places=2)
    min_quantity = PositiveIntegerField(default=10)
    image = ImageField(upload_to='products/')
    # ... ועוד
```

**שיטות חשובות:**
- `is_low_stock()` - בדיקה אם המלאי נמוך
- `profit_margin` - חישוב מרווח רווח

---

### Customer (לקוח)
```python
class Customer(models.Model):
    name = CharField(max_length=200)
    email = EmailField(unique=True)
    phone = CharField(max_length=20)
    customer_type = CharField(choices=CUSTOMER_TYPE_CHOICES)
    is_vip = BooleanField(default=False)
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    total_purchases = DecimalField(max_digits=12, decimal_places=2)
    # ... ועוד
```

**Relations:**
- `Sale` - מכירות הלקוח
- `CustomerNote` - הערות על הלקוח
- `CustomerAlert` - התראות ללקוח

---

### Sale (מכירה)
```python
class Sale(models.Model):
    customer = ForeignKey(Customer)
    sale_date = DateTimeField(auto_now_add=True)
    total_amount = DecimalField(max_digits=12, decimal_places=2)
    tax_amount = DecimalField(max_digits=10, decimal_places=2)
    discount_amount = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(choices=STATUS_CHOICES)
    # ... ועוד
```

**Relations:**
- `SaleItem` - פריטי המכירה

---

### InventoryTransfer (העברת מלאי)
```python
class InventoryTransfer(models.Model):
    from_location = ForeignKey(Location, related_name='transfers_out')
    to_location = ForeignKey(Location, related_name='transfers_in')
    transfer_date = DateTimeField(auto_now_add=True)
    status = CharField(choices=STATUS_CHOICES)
    # ... ועוד
```

**Relations:**
- `TransferItem` - פריטים מועברים

---

## 🎯 Views (תצוגות)

### dashboard (דשבורד)
```python
def dashboard(request):
    """
    מסך ראשי עם סטטיסטיקות

    Returns:
        - total_products: סה"כ מוצרים
        - total_customers: סה"כ לקוחות
        - low_stock_count: מוצרים עם מלאי נמוך
        - recent_sales: מכירות אחרונות
        - alerts: התראות
    """
```

### add_product (הוספת מוצר)
```python
def add_product(request):
    """
    הוספת מוצר חדש

    GET: מציג טופס ריק
    POST: שמירת מוצר חדש

    Form: ProductForm
    Template: product_form.html
    Redirect: product_detail על הצלחה
    """
```

### customer_reports (דוחות לקוחות)
```python
def customer_reports(request):
    """
    דוחות מפורטים על לקוחות

    Aggregations:
        - לקוחות לפי סוג
        - לקוחות לפי עיר
        - לקוחות מובילים (לפי הוצאה)
        - לקוחות לא פעילים

    Returns: JSON data for Chart.js
    """
```

---

## 🛠️ פקודות ניהול (Management Commands)

### backup_database
```bash
python manage.py backup_database [--output-dir DIR]
```
**תיאור:** יוצר גיבוי מלא של מסד הנתונים וקבצי מדיה

**מה נשמר:**
- `db.sqlite3` - מסד נתונים
- `media/` - קבצי מדיה
- `metadata.json` - מטא-דאטה

**שמירה:** `backups/backup_YYYYMMDD_HHMMSS/`

---

### restore_database
```bash
python manage.py restore_database BACKUP_NAME [--backup-dir DIR] [--no-backup]
```
**תיאור:** משחזר מסד נתונים מגיבוי

**אזהרה:** מחליף את מסד הנתונים הנוכחי!

**ברירת מחדל:** יוצר גיבוי של המצב הנוכחי לפני שחזור

---

### list_backups
```bash
python manage.py list_backups [--backup-dir DIR]
```
**תיאור:** מציג רשימת כל הגיבויים הזמינים

**מידע מוצג:**
- שם גיבוי
- תאריך יצירה
- גודל
- מטא-דאטה

---

### view_logs
```bash
python manage.py view_logs [--type TYPE] [--lines N] [--search TERM]
```
**תיאור:** צפייה בלוגים

**פרמטרים:**
- `--type`: general, errors, security, database, all
- `--lines`: מספר שורות אחרונות (ברירת מחדל: 50)
- `--search`: חיפוש טקסט

---

### cleanup_logs
```bash
python manage.py cleanup_logs [--days N] [--compress]
```
**תיאור:** ניקוי לוגים ישנים

**פרמטרים:**
- `--days`: מחיקת לוגים ישנים מ-N ימים (ברירת מחדל: 30)
- `--compress`: דחיסה במקום מחיקה

---

## 🔌 API פנימי

### פונקציות עזר

#### `update_inventory_from_sale(sale)`
```python
def update_inventory_from_sale(sale):
    """
    מעדכן מלאי אחרי מכירה

    Args:
        sale: אובייקט Sale

    Side Effects:
        - מפחית quantity של Product
        - יוצר CustomerSaleHistory
    """
```

#### `complete_transfer(transfer)`
```python
def complete_transfer(transfer):
    """
    משלים העברת מלאי

    Args:
        transfer: אובייקט InventoryTransfer

    Side Effects:
        - מפחית מלאי ממיקום מקור
        - מוסיף מלאי למיקום יעד
        - משנה status ל-completed
    """
```

---

## 🚀 הרחבות עתידיות

### הוספת REST API

1. **התקן Django REST Framework:**
```bash
pip install djangorestframework
```

2. **הוסף ל-INSTALLED_APPS:**
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]
```

3. **צור Serializers:**
```python
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

4. **צור API Views:**
```python
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

5. **הוסף URLs:**
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns += router.urls
```

---

### הוספת אימות משתמשים

1. **צור מודל משתמש מותאם:**
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
```

2. **הגדר ב-settings.py:**
```python
AUTH_USER_MODEL = 'inventory.CustomUser'
```

3. **צור middleware להרשאות:**
```python
class RoleRequiredMixin:
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != self.required_role:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
```

---

### שדרוג ל-PostgreSQL

1. **התקן psycopg2:**
```bash
pip install psycopg2-binary
```

2. **עדכן settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory_db',
        'USER': 'inventory_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **העבר נתונים:**
```bash
# גבה SQLite
python manage.py dumpdata > data.json

# שנה ל-PostgreSQL
python manage.py migrate

# טען נתונים
python manage.py loaddata data.json
```

---

### הוספת Celery למשימות אסינכרוניות

1. **התקן Celery:**
```bash
pip install celery redis
```

2. **צור celery.py:**
```python
from celery import Celery

app = Celery('inventory')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

3. **צור משימות:**
```python
@shared_task
def daily_backup():
    call_command('backup_database')
```

---

## 📝 קונבנציות קוד

### Python Style Guide:
- עקוב אחר PEP 8
- שמות משתנים ב-snake_case
- שמות מחלקות ב-PascalCase
- docstrings לכל פונקציה

### Django Best Practices:
- השתמש ב-QuerySets בצורה יעילה
- הימנע מ-N+1 queries (השתמש ב-select_related/prefetch_related)
- validation בטפסים ו-models
- השתמש ב-transactions למשימות קריטיות

### Git Workflow:
```bash
# עבוד על feature branch
git checkout -b feature/new-feature

# commit messages ברורים
git commit -m "הוסף תכונת X שעושה Y"

# merge ל-main אחרי בדיקה
git checkout main
git merge feature/new-feature
```

---

## 🧪 בדיקות (Tests)

### יצירת בדיקות:
```python
from django.test import TestCase

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            quantity=100
        )

    def test_is_low_stock(self):
        self.product.quantity = 5
        self.assertTrue(self.product.is_low_stock())
```

### הרצת בדיקות:
```bash
python manage.py test
```

---

**גרסה:** 1.0
**עודכן:** 04/10/2025
**למפתחים בלבד**

