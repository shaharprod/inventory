"""
פקודת ניהול לניקוי לוגים ישנים
"""
import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'ניקוי וארכוב לוגים ישנים'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='מחיקת לוגים ישנים מ-X ימים'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='דחיסת לוגים ישנים במקום מחיקה'
        )

    def handle(self, *args, **options):
        days = options['days']
        compress = options['compress']

        logs_dir = settings.LOGS_DIR

        if not os.path.exists(logs_dir):
            self.stdout.write(self.style.WARNING('📁 תיקיית הלוגים לא קיימת'))
            return

        cutoff_date = datetime.now() - timedelta(days=days)

        self.stdout.write(self.style.SUCCESS(f'🧹 מנקה לוגים ישנים מ-{days} ימים'))
        self.stdout.write(f'📅 תאריך חיתוך: {cutoff_date.strftime("%Y-%m-%d %H:%M:%S")}\n')

        cleaned_count = 0
        total_size = 0

        for filename in os.listdir(logs_dir):
            file_path = os.path.join(logs_dir, filename)

            if not os.path.isfile(file_path):
                continue

            # בדיקת תאריך שינוי
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_mtime < cutoff_date:
                file_size = os.path.getsize(file_path)
                total_size += file_size

                if compress:
                    # דחיסה (דורש gzip)
                    import gzip
                    import shutil

                    gz_path = f"{file_path}.gz"
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(gz_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'📦 דחוס: {filename}'))
                else:
                    # מחיקה
                    os.remove(file_path)
                    self.stdout.write(self.style.WARNING(f'🗑️  נמחק: {filename}'))

                cleaned_count += 1

        if cleaned_count > 0:
            size_mb = total_size / (1024 * 1024)
            action = 'דחוסים' if compress else 'נמחקו'
            self.stdout.write(self.style.SUCCESS(f'\n✅ {cleaned_count} קבצים {action}'))
            self.stdout.write(f'💾 שטח פנוי: {size_mb:.2f} MB')
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ אין לוגים ישנים לניקוי'))

