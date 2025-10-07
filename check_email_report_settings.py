#!/usr/bin/env python
"""
בדיקת הגדרות שליחת דוחות
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from inventory.models import SystemSettings

def check_settings():
    """בדיקת הגדרות שליחת דוחות"""

    print("\n" + "="*80)
    print("  🔍 בודק הגדרות שליחת דוחות במייל")
    print("="*80 + "\n")

    try:
        settings = SystemSettings.load()

        print("📧 הגדרות Email:")
        print(f"  • email_enabled: {settings.email_enabled}")
        print(f"  • email_host: {settings.email_host}")
        print(f"  • email_port: {settings.email_port}")
        print(f"  • email_use_tls: {settings.email_use_tls}")
        print(f"  • email_use_ssl: {settings.email_use_ssl}")
        print(f"  • email_host_user: {settings.email_host_user or '(לא מוגדר)'}")
        print(f"  • email_host_password: {'***' if settings.email_host_password else '(לא מוגדר)'}")
        print(f"  • default_from_email: {settings.default_from_email or '(לא מוגדר)'}")

        print("\n📊 הגדרות דוח יומי:")
        print(f"  • daily_report_enabled: {settings.daily_report_enabled}")
        print(f"  • daily_report_email: {settings.daily_report_email or '(לא מוגדר)'}")
        print(f"  • daily_report_time: {settings.daily_report_time}")

        print("\n🚨 הגדרות התראות:")
        print(f"  • alert_email_enabled: {settings.alert_email_enabled}")
        print(f"  • alert_email_recipients: {settings.alert_email_recipients or '(לא מוגדר)'}")

        print("\n" + "="*80)
        print("  ✅ סיכום")
        print("="*80 + "\n")

        # בדיקות
        issues = []

        if not settings.email_enabled:
            issues.append("❌ שליחת מיילים לא מופעלת!")

        if not settings.email_host_user:
            issues.append("❌ לא הוגדר email_host_user (כתובת מייל שולח)")

        if not settings.email_host_password:
            issues.append("❌ לא הוגדר email_host_password (סיסמה/App Password)")

        if not settings.daily_report_email:
            issues.append("⚠️  לא הוגדר daily_report_email (מייל לקבלת דוחות)")

        if issues:
            print("נמצאו בעיות:\n")
            for issue in issues:
                print(f"  {issue}")
            print("\n💡 לתיקון:")
            print("  1. לך לדף הגדרות: http://localhost:8000/settings/")
            print("  2. הפעל 'שליחת מיילים'")
            print("  3. הגדר את פרטי ה-SMTP")
            print("  4. הוסף כתובת מייל לקבלת דוחות")
        else:
            print("✅ כל ההגדרות תקינות!")
            print("\n🎯 כעת תוכל:")
            print("  1. לשלוח דוח מיידי מדף ההגדרות")
            print("  2. להריץ: python manage.py send_daily_report")

        print("\n" + "="*80 + "\n")

    except Exception as e:
        print(f"\n❌ שגיאה: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    check_settings()

