"""
פקודת Django לשליחת דוח יומי במייל
שימוש: python manage.py send_daily_report
"""
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.conf import settings
from inventory.models import (
    Product, Sale, Customer, StockMovement, Alert,
    Category, Supplier, Location
)
import io
import csv
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'שולח דוח יומי מפורט במייל'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='כתובת מייל לשליחה (ברירת מחדל מהגדרות המערכת)',
        )

    def handle(self, *args, **options):
        # טעינת הגדרות מהמסד נתונים
        from inventory.models import SystemSettings
        system_settings = SystemSettings.load()

        # בדיקה אם שליחת מיילים מופעלת
        if not system_settings.email_enabled:
            self.stdout.write(self.style.ERROR('❌ שליחת מיילים לא מופעלת במערכת!'))
            self.stdout.write(self.style.WARNING('הפעל שליחת מיילים בדף "הגדרות"'))
            return

        # קבלת כתובת המייל
        recipient_email = options.get('email') or system_settings.daily_report_email

        if not recipient_email:
            self.stdout.write(self.style.ERROR('❌ לא הוגדר כתובת מייל לקבלת דוחות!'))
            self.stdout.write(self.style.WARNING('הגדר כתובת מייל בדף "הגדרות" או השתמש ב--email'))
            return

        # בדיקת הגדרות SMTP
        if not system_settings.email_host or not system_settings.email_host_user:
            self.stdout.write(self.style.ERROR('❌ לא הוגדרו הגדרות SMTP!'))
            self.stdout.write(self.style.WARNING('הגדר את פרטי השרת בדף "הגדרות"'))
            return

        # עדכון הגדרות Django זמניות מההגדרות במסד הנתונים
        settings.EMAIL_HOST = system_settings.email_host
        settings.EMAIL_PORT = system_settings.email_port
        settings.EMAIL_USE_TLS = system_settings.email_use_tls
        settings.EMAIL_USE_SSL = system_settings.email_use_ssl
        settings.EMAIL_HOST_USER = system_settings.email_host_user
        settings.EMAIL_HOST_PASSWORD = system_settings.email_host_password
        settings.DEFAULT_FROM_EMAIL = system_settings.default_from_email or system_settings.email_host_user

        self.stdout.write(self.style.SUCCESS(f'📧 מכין דוח יומי לשליחה ל-{recipient_email}...'))

        # איסוף נתונים
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # 1. סטטיסטיקות כלליות
        total_products = Product.objects.count()
        low_stock = Product.objects.filter(quantity__lte=F('min_quantity')).count()
        out_of_stock = Product.objects.filter(quantity=0).count()
        total_stock_value = Product.objects.aggregate(
            total=Sum(F('quantity') * F('cost_price'))
        )['total'] or 0

        # 2. מכירות היום
        today_sales = Sale.objects.filter(created_at__date=today)
        daily_sales_count = today_sales.count()
        daily_sales_amount = today_sales.aggregate(total=Sum('total_amount'))['total'] or 0

        # 3. התראות פעילות
        active_alerts = Alert.objects.filter(is_resolved=False).count()
        critical_alerts = Alert.objects.filter(is_resolved=False, severity='critical').count()

        # 4. תנועות מלאי היום
        today_movements = StockMovement.objects.filter(created_at__date=today).count()

        # 5. מוצרים במלאי נמוך (TOP 10)
        low_stock_products = Product.objects.filter(
            quantity__lte=F('min_quantity')
        ).order_by('quantity')[:10]

        # 6. לקוחות פעילים היום
        today_customers = Sale.objects.filter(
            created_at__date=today
        ).values('customer__name').distinct().count()

        # יצירת תוכן HTML למייל
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="he">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; border-right: 4px solid #3498db; padding-right: 10px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
                .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .stat-card.warning {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
                .stat-card.success {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
                .stat-card.info {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }}
                .stat-value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
                .stat-label {{ font-size: 14px; opacity: 0.9; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background-color: #3498db; color: white; padding: 12px; text-align: right; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; text-align: right; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .alert {{ padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .alert-warning {{ background-color: #fff3cd; border-right: 4px solid #ffc107; color: #856404; }}
                .alert-danger {{ background-color: #f8d7da; border-right: 4px solid #dc3545; color: #721c24; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee; text-align: center; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 דוח יומי - מערכת ניהול מלאי</h1>
                <p><strong>תאריך:</strong> {today.strftime('%d/%m/%Y')} | <strong>שעת הפקה:</strong> {timezone.now().strftime('%H:%M')}</p>

                <h2>📈 סטטיסטיקות כלליות</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{total_products}</div>
                        <div class="stat-label">סה"כ מוצרים</div>
                    </div>
                    <div class="stat-card success">
                        <div class="stat-value">₪{total_stock_value:,.0f}</div>
                        <div class="stat-label">ערך מלאי</div>
                    </div>
                    <div class="stat-card warning">
                        <div class="stat-value">{low_stock}</div>
                        <div class="stat-label">מלאי נמוך</div>
                    </div>
                    <div class="stat-card info">
                        <div class="stat-value">{daily_sales_count}</div>
                        <div class="stat-label">מכירות היום</div>
                    </div>
                </div>

                <h2>💰 מכירות היום</h2>
                <div class="stats">
                    <div class="stat-card success">
                        <div class="stat-value">{daily_sales_count}</div>
                        <div class="stat-label">כמות מכירות</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">₪{daily_sales_amount:,.2f}</div>
                        <div class="stat-label">סה"כ מכירות</div>
                    </div>
                    <div class="stat-card info">
                        <div class="stat-value">{today_customers}</div>
                        <div class="stat-label">לקוחות פעילים</div>
                    </div>
                    <div class="stat-card warning">
                        <div class="stat-value">{today_movements}</div>
                        <div class="stat-label">תנועות מלאי</div>
                    </div>
                </div>
        """

        # התראות קריטיות
        if critical_alerts > 0 or out_of_stock > 0:
            html_content += f"""
                <h2>⚠️ התראות חשובות</h2>
            """
            if critical_alerts > 0:
                html_content += f"""
                    <div class="alert alert-danger">
                        <strong>🚨 {critical_alerts} התראות קריטיות!</strong> נדרשת טיפול דחוף.
                    </div>
                """
            if out_of_stock > 0:
                html_content += f"""
                    <div class="alert alert-warning">
                        <strong>📦 {out_of_stock} מוצרים אזלו מהמלאי!</strong> יש להזמין מספקים.
                    </div>
                """

        # מוצרים במלאי נמוך
        if low_stock_products:
            html_content += """
                <h2>📉 מוצרים במלאי נמוך (TOP 10)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>מוצר</th>
                            <th>כמות במלאי</th>
                            <th>מינימום</th>
                            <th>סטטוס</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for product in low_stock_products:
                status = "🔴 אזל" if product.quantity == 0 else "🟡 נמוך"
                html_content += f"""
                        <tr>
                            <td><strong>{product.name}</strong></td>
                            <td>{product.quantity}</td>
                            <td>{product.min_quantity}</td>
                            <td>{status}</td>
                        </tr>
                """
            html_content += """
                    </tbody>
                </table>
            """

        # סיום
        html_content += f"""
                <div class="footer">
                    <p>דוח זה נוצר אוטומטית על ידי מערכת ניהול המלאי</p>
                    <p>© 2024 מערכת ניהול מלאי - כל הזכויות שמורות</p>
                </div>
            </div>
        </body>
        </html>
        """

        # יצירת קבצי CSV מצורפים
        attachments = []

        # 1. קובץ מוצרים במלאי נמוך
        if low_stock_products:
            csv_buffer = io.StringIO()
            csv_buffer.write('\ufeff')  # BOM for Excel
            writer = csv.writer(csv_buffer)
            writer.writerow(['שם מוצר', 'SKU', 'כמות במלאי', 'מינימום', 'קטגוריה', 'ספק'])
            for product in low_stock_products:
                writer.writerow([
                    product.name,
                    product.sku or '',
                    product.quantity,
                    product.min_quantity,
                    product.category.name if product.category else '',
                    product.supplier.name if product.supplier else ''
                ])
            attachments.append(('low_stock_products.csv', csv_buffer.getvalue(), 'text/csv'))

        # 2. קובץ מכירות היום
        if today_sales:
            csv_buffer = io.StringIO()
            csv_buffer.write('\ufeff')
            writer = csv.writer(csv_buffer)
            writer.writerow(['מספר חשבונית', 'לקוח', 'סכום', 'תאריך'])
            for sale in today_sales:
                writer.writerow([
                    sale.invoice_number,
                    sale.customer.name if sale.customer else 'ללא לקוח',
                    f"{sale.total_amount:.2f}",
                    sale.created_at.strftime('%H:%M')
                ])
            attachments.append(('today_sales.csv', csv_buffer.getvalue(), 'text/csv'))

        # שליחת המייל
        try:
            email = EmailMessage(
                subject=f'📊 דוח יומי - {today.strftime("%d/%m/%Y")}',
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            email.content_subtype = 'html'

            # הוספת קבצים מצורפים
            for filename, content, mimetype in attachments:
                email.attach(filename, content, mimetype)

            # שליחת המייל עם טיפול ב-SSL
            import ssl
            import smtplib
            try:
                email.send()
            except Exception as ssl_error:
                # נסה שוב עם אימות SSL מושבת
                if 'CERTIFICATE_VERIFY_FAILED' in str(ssl_error):
                    self.stdout.write(self.style.WARNING('⚠️ בעיית SSL - מנסה שוב ללא אימות תעודות...'))
                    # צור קונטקסט SSL שמתעלם מאימות תעודות
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE

                    # טען הגדרות מהמודל
                    from inventory.models import SystemSettings
                    settings_obj = SystemSettings.load()

                    # שלח ידנית עם ההגדרות המותאמות
                    connection = smtplib.SMTP(settings_obj.email_host, settings_obj.email_port)
                    if settings_obj.email_use_tls:
                        connection.starttls(context=context)
                    connection.login(settings_obj.email_host_user, settings_obj.email_host_password)
                    connection.send_message(email.message())
                    connection.quit()
                else:
                    raise ssl_error

            self.stdout.write(self.style.SUCCESS(f'✅ הדוח נשלח בהצלחה ל-{recipient_email}!'))
            self.stdout.write(self.style.SUCCESS(f'📎 נשלחו {len(attachments)} קבצים מצורפים'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ שגיאה בשליחת המייל: {str(e)}'))
            raise

