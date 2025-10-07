#!/usr/bin/env python
"""
סקריפט לתיקון מוצרים עם ערכי מחיר NULL
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product
from decimal import Decimal

def fix_null_prices():
    """תיקון מוצרים עם ערכי NULL במחירים"""

    print("\n" + "="*80)
    print("  🔧 תיקון ערכי מחיר NULL במוצרים")
    print("="*80 + "\n")

    # מצא מוצרים עם selling_price NULL
    products_null_selling = Product.objects.filter(selling_price__isnull=True)
    count_selling = products_null_selling.count()

    # מצא מוצרים עם cost_price NULL
    products_null_cost = Product.objects.filter(cost_price__isnull=True)
    count_cost = products_null_cost.count()

    print(f"📊 נמצאו:")
    print(f"  • {count_selling} מוצרים עם selling_price = NULL")
    print(f"  • {count_cost} מוצרים עם cost_price = NULL\n")

    if count_selling == 0 and count_cost == 0:
        print("✅ כל המוצרים בסדר - אין ערכי NULL!\n")
        print("="*80 + "\n")
        return

    # תקן selling_price
    if count_selling > 0:
        print(f"🔧 מתקן {count_selling} מוצרים עם selling_price = NULL...")
        for product in products_null_selling:
            product.selling_price = Decimal('0.00')
            product.save()
            print(f"  ✓ {product.name} - selling_price → 0.00")

    # תקן cost_price
    if count_cost > 0:
        print(f"\n🔧 מתקן {count_cost} מוצרים עם cost_price = NULL...")
        for product in products_null_cost:
            product.cost_price = Decimal('0.00')
            product.save()
            print(f"  ✓ {product.name} - cost_price → 0.00")

    print("\n✅ כל המחירים תוקנו!\n")
    print("="*80 + "\n")

    # הצג סיכום
    total_products = Product.objects.count()
    valid_products = Product.objects.filter(
        selling_price__isnull=False,
        cost_price__isnull=False
    ).count()

    print("📈 סיכום:")
    print(f"  • סה\"כ מוצרים: {total_products}")
    print(f"  • מוצרים תקינים: {valid_products}")
    print(f"  • אחוז תקינים: {(valid_products/total_products*100):.1f}%\n")
    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        fix_null_prices()
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

