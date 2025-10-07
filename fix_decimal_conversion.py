#!/usr/bin/env python
"""
תיקון ערכים במסד הנתונים שיהיו Decimal תקינים
"""
import sqlite3
import os

def fix_database():
    """תיקון database ישירות"""
    print("\n" + "="*80)
    print("  🔧 מתקן ערכי Decimal במסד הנתונים")
    print("="*80 + "\n")

    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Database לא נמצא: {db_path}\n")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # תקן products - המר integers ל-Decimal strings
    print("📦 מתקן מוצרים...")

    cursor.execute("SELECT id, name, selling_price, cost_price, margin_percentage FROM inventory_product")
    products = cursor.fetchall()

    for product_id, name, selling_price, cost_price, margin_percentage in products:
        # המר לערכי Decimal תקינים (עם 2 ספרות אחרי הנקודה)
        new_selling = f"{float(selling_price):.2f}" if selling_price is not None else None
        new_cost = f"{float(cost_price):.2f}" if cost_price is not None else None
        new_margin = f"{float(margin_percentage):.2f}" if margin_percentage is not None else None

        print(f"  • {name} (ID: {product_id})")
        print(f"      selling_price: {selling_price} → {new_selling}")
        print(f"      cost_price: {cost_price} → {new_cost}")
        print(f"      margin_percentage: {margin_percentage} → {new_margin}")

        cursor.execute("""
            UPDATE inventory_product
            SET selling_price = ?,
                cost_price = ?,
                margin_percentage = ?
            WHERE id = ?
        """, (new_selling, new_cost, new_margin, product_id))
        print()

    # Commit
    conn.commit()
    print("✅ כל המוצרים עודכנו!\n")

    # בדוק שוב
    print("="*80)
    print("  🔍 מאמת שהתיקון עבד")
    print("="*80 + "\n")

    cursor.execute("SELECT id, name, selling_price, cost_price, margin_percentage FROM inventory_product")
    products = cursor.fetchall()

    for product_id, name, selling_price, cost_price, margin_percentage in products:
        print(f"  • {name} (ID: {product_id})")
        print(f"      selling_price: {selling_price} ({type(selling_price).__name__})")
        print(f"      cost_price: {cost_price} ({type(cost_price).__name__})")
        print(f"      margin_percentage: {margin_percentage} ({type(margin_percentage).__name__})")
        print()

    conn.close()

    print("="*80)
    print("  ✅ התיקון הושלם בהצלחה!")
    print("="*80 + "\n")

if __name__ == '__main__':
    try:
        fix_database()
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()

