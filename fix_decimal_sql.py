#!/usr/bin/env python
"""
תיקון ערכים לא תקינים במחירי מוצרים - SQL ישיר
Fix invalid decimal values using raw SQL
"""
import sqlite3
import sys

def fix_product_prices_sql(db_path='db.sqlite3'):
    """תיקון מחירים לא תקינים בשימוש SQL ישיר"""
    print("\n" + "="*70)
    print("🔧 מתקן ערכים לא תקינים במחירי מוצרים (SQL ישיר)...")
    print("="*70 + "\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # בדיקה כמה מוצרים יש
        cursor.execute("SELECT COUNT(*) FROM inventory_product")
        total = cursor.fetchone()[0]
        print(f"📦 נמצאו {total} מוצרים\n")
        
        # תיקון cost_price
        print("🔧 מתקן cost_price...")
        cursor.execute("""
            UPDATE inventory_product 
            SET cost_price = '0.00' 
            WHERE cost_price IS NULL 
               OR cost_price = '' 
               OR CAST(cost_price AS TEXT) NOT GLOB '[0-9]*.[0-9]*'
        """)
        cost_fixed = cursor.rowcount
        print(f"   ✅ תוקנו {cost_fixed} שדות\n")
        
        # תיקון selling_price
        print("🔧 מתקן selling_price...")
        cursor.execute("""
            UPDATE inventory_product 
            SET selling_price = '0.00' 
            WHERE selling_price IS NULL 
               OR selling_price = '' 
               OR CAST(selling_price AS TEXT) NOT GLOB '[0-9]*.[0-9]*'
        """)
        selling_fixed = cursor.rowcount
        print(f"   ✅ תוקנו {selling_fixed} שדות\n")
        
        # תיקון margin_percentage
        print("🔧 מתקן margin_percentage...")
        cursor.execute("""
            UPDATE inventory_product 
            SET margin_percentage = '0.00' 
            WHERE margin_percentage IS NULL 
               OR margin_percentage = ''
        """)
        margin_fixed = cursor.rowcount
        print(f"   ✅ תוקנו {margin_fixed} שדות\n")
        
        conn.commit()
        conn.close()
        
        print("="*70)
        print(f"✅ תיקון הושלם בהצלחה!")
        print(f"   • cost_price: {cost_fixed} תוקנו")
        print(f"   • selling_price: {selling_fixed} תוקנו")
        print(f"   • margin_percentage: {margin_fixed} תוקנו")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    fix_product_prices_sql()

