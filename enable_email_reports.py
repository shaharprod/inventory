#!/usr/bin/env python
"""
הפעלה מהירה של שליחת דוחות במייל (Console Backend)
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import SystemSettings

def enable_email_reports():
    """הפעל שליחת דוחות עם Console Backend"""

    print("\n" + "="*80)
    print("  📧 מפעיל שליחת דוחות במייל")
    print("="*80 + "\n")

    try:
        settings = SystemSettings.load()

        # הפעל שליחת מיילים (Console Backend)
        settings.email_enabled = True
        settings.email_host = 'localhost'  # לא משנה ב-Console
        settings.email_port = 587
        settings.email_use_tls = True
        settings.email_use_ssl = False
        settings.email_host_user = 'noreply@inventory.local'  # dummy
        settings.email_host_password = 'dummy123'  # dummy
        settings.default_from_email = 'noreply@inventory.local'

        # הפעל דוח יומי
        settings.daily_report_enabled = True
        settings.daily_report_email = 'admin@inventory.local'

        settings.save()

        print("✅ שליחת מיילים הופעלה!")
        print("\n📧 הגדרות נוכחיות:")
        print(f"  • Backend: Console (המיילים יודפסו בקונסול)")
        print(f"  • email_enabled: {settings.email_enabled}")
        print(f"  • daily_report_email: {settings.daily_report_email}")
        print(f"  • daily_report_enabled: {settings.daily_report_enabled}")

        print("\n" + "="*80)
        print("  💡 איך להשתמש:")
        print("="*80 + "\n")

        print("🔹 שליחת דוח מיידי:")
        print("  1. לך ל: http://localhost:8000/settings/")
        print("  2. לחץ על 'שלח דוח מיידי'")
        print("  3. בדוק בחלון השרת (קונסול) - תראה את תוכן המייל\n")

        print("🔹 שליחת דוח יומי (CLI):")
        print("  python manage.py send_daily_report --tenant=1\n")

        print("🔹 למייל אמיתי:")
        print("  1. לך לדף הגדרות: http://localhost:8000/settings/")
        print("  2. הגדר את פרטי Gmail/SMTP")
        print("  3. לקבלת App Password ל-Gmail:")
        print("     https://myaccount.google.com/apppasswords")

        print("\n" + "="*80 + "\n")

    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    enable_email_reports()

