#!/usr/bin/env python
"""
בדיקת ערכי Decimal בעייתיים במוצרים ולקוחות
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import Product, Customer
from decimal import Decimal, InvalidOperation

def check_products():
    """בדיקת מוצרים"""
    print("\n" + "="*80)
    print("  🔍 בודק ערכי Decimal במוצרים")
    print("="*80 + "\n")

    products = Product.objects.all()
    print(f"📦 סה\"כ מוצרים: {products.count()}\n")

    issues = []

    for product in products:
        product_issues = []

        # בדוק selling_price
        try:
            if product.selling_price is not None:
                _ = Decimal(str(product.selling_price))
        except (InvalidOperation, ValueError) as e:
            product_issues.append(f"selling_price: {product.selling_price} ({e})")

        # בדוק cost_price
        try:
            if product.cost_price is not None:
                _ = Decimal(str(product.cost_price))
        except (InvalidOperation, ValueError) as e:
            product_issues.append(f"cost_price: {product.cost_price} ({e})")

        # בדוק margin_percentage
        try:
            if product.margin_percentage is not None:
                _ = Decimal(str(product.margin_percentage))
        except (InvalidOperation, ValueError) as e:
            product_issues.append(f"margin_percentage: {product.margin_percentage} ({e})")

        if product_issues:
            issues.append({
                'product': product,
                'issues': product_issues
            })

    if issues:
        print(f"❌ נמצאו {len(issues)} מוצרים עם בעיות:\n")
        for item in issues:
            print(f"  • {item['product'].name} (ID: {item['product'].id})")
            for issue in item['issues']:
                print(f"    - {issue}")
            print()
    else:
        print("✅ כל המוצרים תקינים!\n")

    return issues

def check_customers():
    """בדיקת לקוחות"""
    print("="*80)
    print("  🔍 בודק ערכי Decimal בלקוחות")
    print("="*80 + "\n")

    customers = Customer.objects.all()
    print(f"👥 סה\"כ לקוחות: {customers.count()}\n")

    issues = []

    for customer in customers:
        customer_issues = []

        # בדוק discount_percent
        try:
            if customer.discount_percent is not None:
                _ = Decimal(str(customer.discount_percent))
        except (InvalidOperation, ValueError) as e:
            customer_issues.append(f"discount_percent: {customer.discount_percent} ({e})")

        # בדוק balance
        try:
            if hasattr(customer, 'balance') and customer.balance is not None:
                _ = Decimal(str(customer.balance))
        except (InvalidOperation, ValueError) as e:
            customer_issues.append(f"balance: {customer.balance} ({e})")

        if customer_issues:
            issues.append({
                'customer': customer,
                'issues': customer_issues
            })

    if issues:
        print(f"❌ נמצאו {len(issues)} לקוחות עם בעיות:\n")
        for item in issues:
            print(f"  • {item['customer'].name} (ID: {item['customer'].id})")
            for issue in item['issues']:
                print(f"    - {issue}")
            print()
    else:
        print("✅ כל הלקוחות תקינים!\n")

    return issues

def main():
    product_issues = check_products()
    customer_issues = check_customers()

    print("="*80)
    print("  📊 סיכום")
    print("="*80 + "\n")
    print(f"  • מוצרים בעייתיים: {len(product_issues)}")
    print(f"  • לקוחות בעייתיים: {len(customer_issues)}")
    print()

    if product_issues or customer_issues:
        print("⚠️  יש צורך בתיקון!\n")
    else:
        print("✅ הכל בסדר!\n")

    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

