"""
סקריפט לחלוקת מלאי כל המוצרים בין מחסן וחנות
מחלק 80% למחסן ו-20% לחנות (ניתן לשנות)
"""
import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product, Location, ProductLocationStock
from django.db import transaction

def distribute_all_products(warehouse_percent=80, store_percent=20):
    """
    חלוקת מלאי כל המוצרים בין מחסן וחנות

    Args:
        warehouse_percent: אחוז למחסן (ברירת מחדל 80%)
        store_percent: אחוז לחנות (ברירת מחדל 20%)
    """
    # קבלת מחסן וחנות
    warehouse = Location.objects.filter(location_type='warehouse', is_active=True).first()
    store = Location.objects.filter(location_type='store', is_active=True).first()

    if not warehouse or not store:
        print("❌ שגיאה: לא נמצא מחסן או חנות פעילים במערכת!")
        return

    print(f"📦 מחסן: {warehouse.name}")
    print(f"🏪 חנות: {store.name}")
    print(f"📊 חלוקה: {warehouse_percent}% מחסן / {store_percent}% חנות")
    print("-" * 60)

    # קבלת כל המוצרים הפעילים עם מלאי
    products = Product.objects.filter(status='active', quantity__gt=0)
    total_products = products.count()

    print(f"📋 נמצאו {total_products} מוצרים לחלוקה\n")

    updated_count = 0
    skipped_count = 0

    with transaction.atomic():
        for i, product in enumerate(products, 1):
            try:
                total_quantity = product.quantity

                # חישוב כמויות
                warehouse_qty = int(total_quantity * warehouse_percent / 100)
                store_qty = total_quantity - warehouse_qty

                # יצירה/עדכון מלאי במחסן
                warehouse_stock, created = ProductLocationStock.objects.get_or_create(
                    product=product,
                    location=warehouse,
                    defaults={'quantity': warehouse_qty}
                )
                if not created:
                    warehouse_stock.quantity = warehouse_qty
                    warehouse_stock.save()

                # יצירה/עדכון מלאי בחנות
                store_stock, created = ProductLocationStock.objects.get_or_create(
                    product=product,
                    location=store,
                    defaults={'quantity': store_qty}
                )
                if not created:
                    store_stock.quantity = store_qty
                    store_stock.save()

                print(f"✅ [{i}/{total_products}] {product.name}")
                print(f"   סה\"כ: {total_quantity} → מחסן: {warehouse_qty} | חנות: {store_qty}")

                updated_count += 1

            except Exception as e:
                print(f"❌ [{i}/{total_products}] שגיאה ב-{product.name}: {str(e)}")
                skipped_count += 1

    print("\n" + "=" * 60)
    print(f"✅ הושלם!")
    print(f"📊 סטטיסטיקה:")
    print(f"   • מוצרים שעודכנו: {updated_count}")
    print(f"   • מוצרים שדולגו: {skipped_count}")
    print(f"   • סה\"כ מוצרים: {total_products}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 חלוקת מלאי אוטומטית לכל המוצרים")
    print("=" * 60)
    print()

    # שאלה למשתמש
    print("📋 אפשרויות חלוקה:")
    print("1. 80% מחסן / 20% חנות (ברירת מחדל)")
    print("2. 60% מחסן / 40% חנות")
    print("3. 50% מחסן / 50% חנות")
    print("4. התאמה אישית")
    print()

    choice = input("בחר אפשרות (1-4) או Enter לברירת מחדל: ").strip()

    if choice == "2":
        warehouse_percent = 60
        store_percent = 40
    elif choice == "3":
        warehouse_percent = 50
        store_percent = 50
    elif choice == "4":
        try:
            warehouse_percent = int(input("אחוז למחסן (0-100): "))
            store_percent = 100 - warehouse_percent
            if warehouse_percent < 0 or warehouse_percent > 100:
                raise ValueError()
        except:
            print("❌ ערך לא תקין! משתמש בברירת מחדל (80/20)")
            warehouse_percent = 80
            store_percent = 20
    else:
        warehouse_percent = 80
        store_percent = 20

    print()
    confirm = input(f"⚠️  האם לחלק את כל המוצרים ל-{warehouse_percent}% מחסן / {store_percent}% חנות? (yes/no): ").strip().lower()

    if confirm in ['yes', 'y', 'כן']:
        print()
        distribute_all_products(warehouse_percent, store_percent)
    else:
        print("❌ פעולה בוטלה.")

