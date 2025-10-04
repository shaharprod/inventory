"""
פקודת ניהול לגיבוי מסד הנתונים
"""
import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import json


class Command(BaseCommand):
    help = 'גיבוי מסד הנתונים והקבצים החשובים'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='backups',
            help='תיקיית היעד לגיבויים'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']

        # יצירת תיקיית גיבויים אם לא קיימת
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.stdout.write(self.style.SUCCESS(f'✅ נוצרה תיקיית גיבויים: {output_dir}'))

        # שם גיבוי עם תאריך ושעה
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = os.path.join(output_dir, backup_name)

        # יצירת תיקיית הגיבוי הספציפי
        os.makedirs(backup_path)

        self.stdout.write(self.style.WARNING(f'🔄 מתחיל גיבוי: {backup_name}'))

        try:
            # 1. גיבוי מסד הנתונים
            self.backup_database(backup_path)

            # 2. גיבוי קבצי מדיה (אם קיימים)
            self.backup_media(backup_path)

            # 3. יצירת קובץ מטא-דאטה
            self.create_metadata(backup_path)

            # 4. ניקוי גיבויים ישנים (שומר 30 האחרונים)
            self.cleanup_old_backups(output_dir, keep=30)

            self.stdout.write(self.style.SUCCESS(f'✅ הגיבוי הושלם בהצלחה: {backup_path}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ שגיאה בגיבוי: {str(e)}'))
            # מחיקת גיבוי לא שלם
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            raise

    def backup_database(self, backup_path):
        """גיבוי מסד הנתונים"""
        db_path = settings.DATABASES['default']['NAME']

        if os.path.exists(db_path):
            backup_db_path = os.path.join(backup_path, 'db.sqlite3')
            shutil.copy2(db_path, backup_db_path)

            # חישוב גודל הקובץ
            size_mb = os.path.getsize(backup_db_path) / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(f'  ✅ מסד נתונים: {size_mb:.2f} MB'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  מסד נתונים לא נמצא'))

    def backup_media(self, backup_path):
        """גיבוי קבצי מדיה"""
        media_root = settings.MEDIA_ROOT

        if os.path.exists(media_root) and os.listdir(media_root):
            backup_media_path = os.path.join(backup_path, 'media')
            shutil.copytree(media_root, backup_media_path)

            # ספירת קבצים
            file_count = sum([len(files) for r, d, files in os.walk(backup_media_path)])
            self.stdout.write(self.style.SUCCESS(f'  ✅ קבצי מדיה: {file_count} קבצים'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  אין קבצי מדיה לגיבוי'))

    def create_metadata(self, backup_path):
        """יצירת קובץ מטא-דאטה"""
        metadata = {
            'backup_date': datetime.now().isoformat(),
            'django_version': settings.ALLOWED_HOSTS,
            'database': settings.DATABASES['default']['ENGINE'],
            'backup_version': '1.0'
        }

        metadata_path = os.path.join(backup_path, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS('  ✅ מטא-דאטה נוצר'))

    def cleanup_old_backups(self, output_dir, keep=30):
        """מחיקת גיבויים ישנים"""
        backups = []
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path) and item.startswith('backup_'):
                backups.append((item_path, os.path.getctime(item_path)))

        # מיון לפי תאריך יצירה
        backups.sort(key=lambda x: x[1], reverse=True)

        # מחיקת הגיבויים הישנים
        deleted_count = 0
        for backup_path, _ in backups[keep:]:
            shutil.rmtree(backup_path)
            deleted_count += 1

        if deleted_count > 0:
            self.stdout.write(self.style.WARNING(f'  🗑️  נמחקו {deleted_count} גיבויים ישנים'))

