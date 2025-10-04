#!/usr/bin/env python
"""
תיקון ערכים לא תקינים במחירי מוצרים
Fix invalid decimal values in product prices
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product
from decimal import Decimal, InvalidOperation

def fix_product_prices():
    """תיקון מחירים לא תקינים במוצרים"""
    print("\n" + "="*70)
    print("🔧 מתקן ערכים לא תקינים במחירי מוצרים...")
    print("="*70 + "\n")
    
    fixed_count = 0
    error_count = 0
    
    for product in Product.objects.all():
        changed = False
        errors = []
        
        # בדיקה ותיקון cost_price
        try:
            if product.cost_price is None:
                product.cost_price = Decimal('0.00')
                changed = True
                errors.append(f"cost_price: None → 0.00")
            elif not isinstance(product.cost_price, Decimal):
                product.cost_price = Decimal(str(product.cost_price))
                changed = True
                errors.append(f"cost_price: המרה ל-Decimal")
        except (ValueError, InvalidOperation) as e:
            product.cost_price = Decimal('0.00')
            changed = True
            errors.append(f"cost_price: ERROR ({e}) → 0.00")
            error_count += 1
        
        # בדיקה ותיקון selling_price
        try:
            if product.selling_price is None:
                product.selling_price = Decimal('0.00')
                changed = True
                errors.append(f"selling_price: None → 0.00")
            elif not isinstance(product.selling_price, Decimal):
                product.selling_price = Decimal(str(product.selling_price))
                changed = True
                errors.append(f"selling_price: המרה ל-Decimal")
        except (ValueError, InvalidOperation) as e:
            product.selling_price = Decimal('0.00')
            changed = True
            errors.append(f"selling_price: ERROR ({e}) → 0.00")
            error_count += 1
        
        # שמירה אם היו שינויים
        if changed:
            try:
                product.save()
                fixed_count += 1
                print(f"✅ {product.name} (ID: {product.id})")
                for error in errors:
                    print(f"   └─ {error}")
            except Exception as e:
                print(f"❌ שגיאה בשמירת {product.name}: {e}")
                error_count += 1
    
    print("\n" + "="*70)
    print(f"✅ תוקנו {fixed_count} מוצרים")
    if error_count > 0:
        print(f"⚠️  {error_count} שגיאות")
    print("="*70 + "\n")

if __name__ == '__main__':
    fix_product_prices()

