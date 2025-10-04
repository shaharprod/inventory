"""
סקריפט לתיקון כמויות מוצרים - סנכרון מלאי כללי עם מחסן וחנות
"""
import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product, ProductLocationStock
from django.db.models import Sum

def fix_all_product_quantities():
    """סנכרון כמויות כלליות של כל המוצרים"""

    print("=" * 70)
    print("🔧 תיקון וסנכרון כמויות מוצרים")
    print("=" * 70)
    print()

    products = Product.objects.all()
    fixed_count = 0

    for product in products:
        # חישוב סכום מלאי בכל המיקומים
        total_from_locations = ProductLocationStock.objects.filter(
            product=product
        ).aggregate(total=Sum('quantity'))['total'] or 0

        old_quantity = product.quantity

        # אם יש הבדל, תקן
        if old_quantity != total_from_locations:
            product.quantity = total_from_locations
            product.save(update_fields=['quantity'])

            print(f"✅ {product.name}")
            print(f"   ישן: {old_quantity} → חדש: {total_from_locations}")

            # הצג פירוט מיקומים
            location_stocks = ProductLocationStock.objects.filter(product=product)
            for ls in location_stocks:
                print(f"   • {ls.location.get_location_type_display()}: {ls.quantity}")
            print()

            fixed_count += 1

    print("=" * 70)
    print(f"✅ הושלם! תוקנו {fixed_count} מוצרים")
    print("=" * 70)

if __name__ == "__main__":
    fix_all_product_quantities()

