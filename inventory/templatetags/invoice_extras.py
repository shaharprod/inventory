"""
Template filters למחירים עם מע"מ
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='divide_vat')
def divide_vat(value, tax_rate):
    """
    מחלק מחיר (כולל מע"מ) כדי לקבל מחיר לפני מע"מ

    נוסחה: מחיר לפני מע"מ = מחיר כולל / (1 + tax_rate/100)

    דוגמה: 118 ₪ עם 18% מע"מ = 100 ₪ לפני מע"מ
    """
    try:
        value = Decimal(str(value))
        tax_rate = Decimal(str(tax_rate))

        # מחיר לפני מע"מ
        price_before_vat = value / (1 + tax_rate / 100)
        return price_before_vat
    except (ValueError, TypeError, ZeroDivisionError):
        return value


@register.filter(name='extract_vat')
def extract_vat(value, tax_rate):
    """
    מחלץ את סכום המע"מ ממחיר כולל מע"מ

    נוסחה:
    1. מחיר לפני מע"מ = מחיר כולל / (1 + tax_rate/100)
    2. סכום מע"מ = מחיר כולל - מחיר לפני מע"מ

    דוגמה: 118 ₪ עם 18% מע"מ = 18 ₪ מע"מ
    """
    try:
        value = Decimal(str(value))
        tax_rate = Decimal(str(tax_rate))

        # מחיר לפני מע"מ
        price_before_vat = value / (1 + tax_rate / 100)

        # סכום המע"מ
        vat_amount = value - price_before_vat
        return vat_amount
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter(name='mul')
def multiply(value, arg):
    """כפל פשוט"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return value


@register.filter(name='div')
def divide(value, arg):
    """חלוקה פשוטה"""
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError, ZeroDivisionError):
        return value


@register.filter(name='add_decimal')
def add_decimal(value, arg):
    """חיבור מדויק עם Decimal"""
    try:
        return Decimal(str(value)) + Decimal(str(arg))
    except (ValueError, TypeError):
        return value

