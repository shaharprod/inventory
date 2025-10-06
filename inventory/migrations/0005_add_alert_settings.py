# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_systemsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsettings',
            name='low_stock_threshold',
            field=models.IntegerField(default=10, help_text='כמות מינימלית להתראה', verbose_name='סף מלאי נמוך'),
        ),
        migrations.AddField(
            model_name='systemsettings',
            name='critical_stock_threshold',
            field=models.IntegerField(default=5, help_text='כמות קריטית להתראה דחופה', verbose_name='סף מלאי קריטי'),
        ),
        migrations.AddField(
            model_name='systemsettings',
            name='enable_low_stock_alerts',
            field=models.BooleanField(default=True, verbose_name='הפעל התראות מלאי נמוך'),
        ),
        migrations.AddField(
            model_name='systemsettings',
            name='enable_expiry_alerts',
            field=models.BooleanField(default=True, verbose_name='הפעל התראות תפוגה'),
        ),
        migrations.AddField(
            model_name='systemsettings',
            name='expiry_alert_days',
            field=models.IntegerField(default=30, help_text='התרע X ימים לפני תאריך תפוגה', verbose_name='ימים לפני תפוגה'),
        ),
    ]

