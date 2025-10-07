"""
סקריפט לסימון כל המנהלים כמאומתים
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("🔧 מסמן מנהלים כמאומתים")
print("="*80)

# מצא את כל המשתמשים שהם superuser
superusers = User.objects.filter(is_superuser=True)

if not superusers.exists():
    print("\n❌ לא נמצאו מנהלי מערכת!")
else:
    print(f"\n📊 נמצאו {superusers.count()} מנהלי מערכת:\n")

    for user in superusers:
        # סמן את המייל כמאומת
        if not user.email_verified:
            user.email_verified = True
            user.save()
            print(f"✅ {user.username} - המייל סומן כמאומת")
        else:
            print(f"✓ {user.username} - המייל כבר מאומת")

print("\n" + "="*80)
print("✅ הושלם! כל המנהלים מאומתים!")
print("="*80)
print("\n💡 עכשיו תוכל להתחבר בלי בעיות!")
print()

