"""
סקריפט מהיר לחלוקת מלאי כל המוצרים בין מחסן וחנות
80% מחסן / 20% חנות
"""
import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product, Location, ProductLocationStock
from django.db import transaction

def distribute_all_products():
    """חלוקת מלאי כל המוצרים: 80% מחסן / 20% חנות"""

    # קבלת מחסן וחנות
    warehouse = Location.objects.filter(location_type='warehouse', is_active=True).first()
    store = Location.objects.filter(location_type='store', is_active=True).first()

    if not warehouse or not store:
        print("❌ שגיאה: לא נמצא מחסן או חנות פעילים במערכת!")
        return

    print("=" * 70)
    print("🔄 חלוקת מלאי אוטומטית לכל המוצרים")
    print("=" * 70)
    print(f"📦 מחסן: {warehouse.name}")
    print(f"🏪 חנות: {store.name}")
    print(f"📊 חלוקה: 80% מחסן / 20% חנות")
    print("-" * 70)

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

                # חישוב כמויות: 80% מחסן, 20% חנות
                warehouse_qty = int(total_quantity * 0.8)
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
                print(f"   סה\"כ: {total_quantity} → מחסן: {warehouse_qty} ({warehouse_qty}/{total_quantity}) | חנות: {store_qty} ({store_qty}/{total_quantity})")

                updated_count += 1

            except Exception as e:
                print(f"❌ [{i}/{total_products}] שגיאה ב-{product.name}: {str(e)}")
                skipped_count += 1

    print("\n" + "=" * 70)
    print(f"✅ הושלם!")
    print(f"📊 סטטיסטיקה:")
    print(f"   • מוצרים שעודכנו: {updated_count}")
    print(f"   • מוצרים שדולגו: {skipped_count}")
    print(f"   • סה\"כ מוצרים: {total_products}")
    print("=" * 70)

if __name__ == "__main__":
    distribute_all_products()

