#!/usr/bin/env python
"""
החזרת EMAIL_BACKEND ל-Console
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("  🔧 מחליף ל-Console Email Backend")
print("="*80 + "\n")

print(f"📧 Backend נוכחי: {settings.EMAIL_BACKEND}")

# עדכון settings
settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print(f"✅ Backend חדש: {settings.EMAIL_BACKEND}")

print("\n💡 עכשיו דוחות יודפסו בטרמינל של Django!")
print("   לא צריך Gmail App Password.\n")

print("="*80 + "\n")

