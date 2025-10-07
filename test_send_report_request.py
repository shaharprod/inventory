#!/usr/bin/env python
"""
סימולציה מלאה של request ל-send_instant_report
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from inventory.views import send_instant_report
from inventory.models import Tenant
import json

print("\n" + "="*80)
print("  🧪 בדיקת send_instant_report - סימולציה מלאה")
print("="*80 + "\n")

User = get_user_model()

# יצירת request מזויף
factory = RequestFactory()
request = factory.post('/send-instant-report/')

# הוספת user
try:
    user = User.objects.first()
    if user:
        request.user = user
        print(f"✅ User: {user.username}")
    else:
        print("⚠️  אין user - ממשיך ללא")
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
except Exception as e:
    print(f"⚠️  שגיאה ב-User: {e}")
    from django.contrib.auth.models import AnonymousUser
    request.user = AnonymousUser()

# הוספת tenant
try:
    tenant = Tenant.objects.first()
    if tenant:
        request.tenant = tenant
        print(f"✅ Tenant: {tenant.name}")
except Exception as e:
    print(f"⚠️  שגיאה ב-Tenant: {e}")

print("\n📞 קורא ל-send_instant_report()...\n")

# קריאה לפונקציה
try:
    response = send_instant_report(request)

    print("✅ הפונקציה הוחזרה בהצלחה!\n")
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.get('Content-Type', 'לא מוגדר')}\n")

    # פענוח JSON
    try:
        data = json.loads(response.content)
        print("📊 תוכן התשובה:")
        print(f"  success: {data.get('success')}")
        if data.get('success'):
            print(f"  message: {data.get('message')}")
            if 'details' in data:
                print(f"  details: {data.get('details')}")
        else:
            print(f"  error: {data.get('error')}")
    except json.JSONDecodeError as e:
        print(f"❌ לא JSON תקין!")
        print(f"   התוכן: {response.content[:200]}")

except Exception as e:
    print(f"❌ שגיאה בפונקציה: {e}\n")
    import traceback
    traceback.print_exc()

print("\n" + "="*80 + "\n")

