#!/usr/bin/env python
"""
בדיקת ערכי Decimal ישירות מה-database
"""
import sqlite3
import os

def check_database():
    """בדיקת database ישירות"""
    print("\n" + "="*80)
    print("  🔍 בודק database ישירות (ללא Django ORM)")
    print("="*80 + "\n")

    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Database לא נמצא: {db_path}\n")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # בדוק products
    print("📦 בודק מוצרים...")
    cursor.execute("""
        SELECT id, name, selling_price, cost_price, margin_percentage
        FROM inventory_product
    """)

    products = cursor.fetchall()
    print(f"  סה\"כ: {len(products)} מוצרים\n")

    issues = []
    for row in products:
        product_id, name, selling_price, cost_price, margin_percentage = row
        row_issues = []

        # בדוק כל ערך
        if selling_price is not None and not isinstance(selling_price, (int, float)):
            row_issues.append(f"selling_price: '{selling_price}' (type: {type(selling_price).__name__})")

        if cost_price is not None and not isinstance(cost_price, (int, float)):
            row_issues.append(f"cost_price: '{cost_price}' (type: {type(cost_price).__name__})")

        if margin_percentage is not None and not isinstance(margin_percentage, (int, float)):
            row_issues.append(f"margin_percentage: '{margin_percentage}' (type: {type(margin_percentage).__name__})")

        if row_issues:
            issues.append({
                'id': product_id,
                'name': name,
                'issues': row_issues
            })

        # הצג את כל המוצרים
        print(f"  • ID {product_id}: {name}")
        print(f"      selling_price: {selling_price} ({type(selling_price).__name__})")
        print(f"      cost_price: {cost_price} ({type(cost_price).__name__})")
        print(f"      margin_percentage: {margin_percentage} ({type(margin_percentage).__name__})")
        print()

    if issues:
        print(f"\n❌ נמצאו {len(issues)} מוצרים עם בעיות:\n")
        for item in issues:
            print(f"  • ID {item['id']}: {item['name']}")
            for issue in item['issues']:
                print(f"    - {issue}")
            print()
    else:
        print("✅ כל הערכים נראים תקינים (כ-numbers)!\n")

    # בדוק לקוחות
    print("="*80)
    print("👥 בודק לקוחות...")
    cursor.execute("""
        SELECT id, name, discount_percent
        FROM inventory_customer
    """)

    customers = cursor.fetchall()
    print(f"  סה\"כ: {len(customers)} לקוחות\n")

    for row in customers:
        customer_id, name, discount_percent = row
        print(f"  • ID {customer_id}: {name}")
        print(f"      discount_percent: {discount_percent} ({type(discount_percent).__name__})")
        print()

    conn.close()

    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        check_database()
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()

