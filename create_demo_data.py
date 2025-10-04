"""
סקריפט ליצירת נתוני דמו למערכת ניהול המלאי
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import (
    Category, Supplier, Location, Product, Customer,
    ProductLocationStock, CompanySettings
)
from django.contrib.auth.models import User
from decimal import Decimal

def create_demo_data():
    print("\n🎨 יוצר נתוני דמו...")
    print("="*70)

    # 1. הגדרות חברה
    print("\n1️⃣ יוצר הגדרות חברה...")
    company, created = CompanySettings.objects.get_or_create(
        business_number="123456789",
        defaults={
            'company_name': 'חברת המלאי בע"מ',
            'tax_id': '512345678',
            'address': 'רחוב הראשי 123',
            'city': 'תל אביב',
            'postal_code': '6789012',
            'phone': '03-1234567',
            'email': 'info@inventory.co.il',
            'website': 'https://inventory.co.il',
            'invoice_prefix': 'INV',
            'current_invoice_number': 1,
            'default_tax_rate': Decimal('18.00'),
        }
    )
    print(f"   ✓ {company.company_name}")

    # 2. קטגוריות
    print("\n2️⃣ יוצר קטגוריות...")
    categories_data = [
        ('אלקטרוניקה', 'מוצרי אלקטרוניקה וחשמל'),
        ('ביגוד', 'בגדים והנעלה'),
        ('מזון', 'מוצרי מזון ומשקאות'),
        ('ריהוט', 'רהיטים לבית ולמשרד'),
        ('ספרים', 'ספרים ומגזינים'),
    ]

    categories = {}
    for name, desc in categories_data:
        cat, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        categories[name] = cat
        print(f"   ✓ {name}")

    # 3. ספקים
    print("\n3️⃣ יוצר ספקים...")
    suppliers_data = [
        ('ספק אלקטרוניקה', 'יוסי כהן', '03-9876543', 'yossi@electronics.co.il'),
        ('ספק ביגוד', 'דנה לוי', '04-1234567', 'dana@fashion.co.il'),
        ('ספק מזון', 'משה דוד', '02-9876543', 'moshe@food.co.il'),
    ]

    suppliers = {}
    for name, contact, phone, email in suppliers_data:
        sup, created = Supplier.objects.get_or_create(
            name=name,
            defaults={
                'contact_person': contact,
                'phone': phone,
                'email': email,
                'is_active': True
            }
        )
        suppliers[name] = sup
        print(f"   ✓ {name}")

    # 4. מיקומים
    print("\n4️⃣ יוצר מיקומים...")
    warehouse, created = Location.objects.get_or_create(
        name='מחסן ראשי',
        defaults={
            'location_type': 'warehouse',
            'address': 'אזור תעשייה, רחוב המלאכה 45',
            'city': 'פתח תקווה',
            'capacity': 10000,
            'is_active': True,
            'is_main_warehouse': True,
        }
    )
    print(f"   ✓ {warehouse.name}")

    store, created = Location.objects.get_or_create(
        name='חנות ראשית',
        defaults={
            'location_type': 'store',
            'address': 'דיזנגוף 123',
            'city': 'תל אביב',
            'capacity': 2000,
            'is_active': True,
            'is_main_store': True,
        }
    )
    print(f"   ✓ {store.name}")

    # 5. מוצרים
    print("\n5️⃣ יוצר מוצרים...")
    products_data = [
        ('מחשב נייד Dell', 'אלקטרוניקה', 'ספק אלקטרוניקה', 3500, 4200, 15, 5, 50, 'LAP001', '7290001234567'),
        ('עכבר אלחוטי', 'אלקטרוניקה', 'ספק אלקטרוניקה', 45, 89, 100, 20, 200, 'MOU001', '7290001234568'),
        ('חולצת פולו', 'ביגוד', 'ספק ביגוד', 80, 149, 50, 10, 100, 'POL001', '7290001234569'),
        ('ג\'ינס כחול', 'ביגוד', 'ספק ביגוד', 120, 249, 40, 10, 100, 'JEA001', '7290001234570'),
        ('בקבוק מים 1.5L', 'מזון', 'ספק מזון', 3, 7, 500, 100, 1000, 'WAT001', '7290001234571'),
        ('חטיף בריאות', 'מזון', 'ספק מזון', 5, 12, 200, 50, 500, 'SNA001', '7290001234572'),
        ('כיסא משרדי', 'ריהוט', 'ספק אלקטרוניקה', 250, 499, 25, 5, 50, 'CHA001', '7290001234573'),
        ('שולחן כתיבה', 'ריהוט', 'ספק אלקטרוניקה', 450, 899, 15, 3, 30, 'DES001', '7290001234574'),
        ('ספר בדיון', 'ספרים', 'ספק ביגוד', 35, 69, 80, 20, 150, 'BOO001', '7290001234575'),
        ('מגזין טכנולוגיה', 'ספרים', 'ספק ביגוד', 15, 29, 60, 15, 100, 'MAG001', '7290001234576'),
    ]

    for name, cat_name, sup_name, cost, price, qty, min_qty, max_qty, sku, barcode in products_data:
        product, created = Product.objects.get_or_create(
            sku=sku,
            defaults={
                'name': name,
                'category': categories[cat_name],
                'supplier': suppliers[sup_name],
                'quantity': qty,
                'min_quantity': min_qty,
                'max_quantity': max_qty,
                'cost_price': Decimal(str(cost)),
                'selling_price': Decimal(str(price)),
                'barcode': barcode,
                'unit': 'pcs',
                'status': 'active',
            }
        )

        # חלוקת מלאי: 70% מחסן, 30% חנות
        warehouse_qty = int(qty * 0.7)
        store_qty = qty - warehouse_qty

        ProductLocationStock.objects.get_or_create(
            product=product,
            location=warehouse,
            defaults={'quantity': warehouse_qty, 'min_quantity': min_qty}
        )

        ProductLocationStock.objects.get_or_create(
            product=product,
            location=store,
            defaults={'quantity': store_qty, 'min_quantity': int(min_qty * 0.3)}
        )

        print(f"   ✓ {name} (מחסן: {warehouse_qty}, חנות: {store_qty})")

    # 6. לקוחות
    print("\n6️⃣ יוצר לקוחות...")
    customers_data = [
        ('דוד כהן', 'individual', '054-1234567', 'david@gmail.com', 'רמת גן', 5),
        ('שרה לוי', 'individual', '052-9876543', 'sara@gmail.com', 'תל אביב', 10),
        ('חברת הטכנולוגיה בע"מ', 'business', '03-6543210', 'info@tech.co.il', 'הרצליה', 15),
        ('מסעדת הבשר', 'business', '04-8765432', 'meat@restaurant.co.il', 'חיפה', 8),
    ]

    for name, ctype, phone, email, city, discount in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'customer_type': ctype,
                'phone': phone,
                'city': city,
                'discount_percent': Decimal(str(discount)),
                'is_active': True,
            }
        )
        print(f"   ✓ {name}")

    print("\n" + "="*70)
    print("✅ נתוני הדמו נוצרו בהצלחה!")
    print("\n📊 סיכום:")
    print(f"   • קטגוריות: {Category.objects.count()}")
    print(f"   • ספקים: {Supplier.objects.count()}")
    print(f"   • מיקומים: {Location.objects.count()}")
    print(f"   • מוצרים: {Product.objects.count()}")
    print(f"   • לקוחות: {Customer.objects.count()}")
    print(f"   • רשומות מלאי לפי מיקום: {ProductLocationStock.objects.count()}")

if __name__ == '__main__':
    create_demo_data()

