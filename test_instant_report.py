#!/usr/bin/env python
"""
בדיקת שליחת דוח מיידי - סימולציה
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import SystemSettings, Product, Sale, Alert, StockMovement, Tenant
from django.utils import timezone
from django.db.models import Sum, F

def test_instant_report():
    """בדיקת שליחת דוח מיידי"""

    print("\n" + "="*80)
    print("  🧪 בודק שליחת דוח מיידי")
    print("="*80 + "\n")

    try:
        # קבל tenant ראשון
        tenant = Tenant.objects.first()
        if not tenant:
            print("⚠️  אין tenants במערכת. יוצר tenant לדוגמה...")
            from inventory.models import CustomUser
            user = CustomUser.objects.first()
            if user:
                tenant = Tenant.objects.create(
                    name="Test Company",
                    slug="test-company",
                    email="test@example.com",
                    owner=user,
                    status='active'
                )
                print(f"✅ נוצר tenant: {tenant.name}")
            else:
                print("❌ אין משתמשים במערכת!")
                return

        print(f"📦 Tenant: {tenant.name}\n")

        # בדוק הגדרות
        settings_obj = SystemSettings.load()

        print("📧 בודק הגדרות Email:")
        print(f"  • email_enabled: {settings_obj.email_enabled}")
        print(f"  • daily_report_email: {settings_obj.daily_report_email}")

        if not settings_obj.email_enabled:
            print("\n❌ שליחת מיילים לא מופעלת!")
            return

        if not settings_obj.daily_report_email:
            print("\n❌ לא הוגדר daily_report_email!")
            return

        print("\n✅ הגדרות Email תקינות\n")

        # סינון לפי tenant
        print(f"📊 איסוף נתונים עבור {tenant.name}:")

        products_qs = Product.objects.filter(tenant=tenant)
        sales_qs = Sale.objects.filter(tenant=tenant)

        total_products = products_qs.count()
        low_stock = products_qs.filter(quantity__lte=F('min_quantity')).count()
        out_of_stock = products_qs.filter(quantity=0).count()

        today = timezone.now().date()
        today_sales = sales_qs.filter(created_at__date=today)
        daily_sales_count = today_sales.count()

        print(f"  • סה\"כ מוצרים: {total_products}")
        print(f"  • מלאי נמוך: {low_stock}")
        print(f"  • אזל מהמלאי: {out_of_stock}")
        print(f"  • מכירות היום: {daily_sales_count}")

        print("\n✅ איסוף נתונים הצליח!")
        print("\n💡 הפונקציה send_instant_report צריכה לעבוד כעת.")
        print("   נסה שוב מהדפדפן.")

    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    test_instant_report()

