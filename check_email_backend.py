#!/usr/bin/env python
"""
בדיקה מהירה - איזה EMAIL_BACKEND בשימוש?
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("  📧 בדיקת EMAIL_BACKEND")
print("="*80 + "\n")

backend = settings.EMAIL_BACKEND
print(f"EMAIL_BACKEND: {backend}\n")

if 'console' in backend.lower():
    print("✅ Console Backend - דוחות יודפסו בטרמינל!")
    print("   זה בדיוק מה שאנחנו רוצים.\n")
elif 'smtp' in backend.lower():
    print("⚠️  SMTP Backend - ינסה לשלוח דרך Gmail")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}\n")
else:
    print(f"⚠️  Backend לא מזוהה: {backend}\n")

print("="*80 + "\n")

