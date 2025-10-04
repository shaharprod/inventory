"""
פקודת ניהול לשחזור מסד הנתונים
"""
import os
import shutil
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'שחזור מסד הנתונים מגיבוי'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_name',
            type=str,
            help='שם תיקיית הגיבוי לשחזור (לדוגמה: backup_20250104_120000)'
        )
        parser.add_argument(
            '--backup-dir',
            type=str,
            default='backups',
            help='תיקיית הגיבויים'
        )
        parser.add_argument(
            '--no-backup',
            action='store_true',
            help='לא לבצע גיבוי לפני השחזור'
        )

    def handle(self, *args, **options):
        backup_name = options['backup_name']
        backup_dir = options['backup_dir']
        no_backup = options['no_backup']

        backup_path = os.path.join(backup_dir, backup_name)

        # בדיקת קיום הגיבוי
        if not os.path.exists(backup_path):
            self.stdout.write(self.style.ERROR(f'❌ הגיבוי לא נמצא: {backup_path}'))
            self.list_available_backups(backup_dir)
            return

        # בדיקת תקינות הגיבוי
        if not self.validate_backup(backup_path):
            self.stdout.write(self.style.ERROR('❌ הגיבוי לא תקין'))
            return

        # אזהרה למשתמש
        self.stdout.write(self.style.WARNING('⚠️  שחזור מסד נתונים ימחק את כל המידע הנוכחי!'))

        # גיבוי מצב נוכחי לפני שחזור (אלא אם צוין אחרת)
        if not no_backup:
            self.stdout.write(self.style.WARNING('🔄 מבצע גיבוי של המצב הנוכחי לפני השחזור...'))
            from django.core.management import call_command
            call_command('backup_database', output_dir=backup_dir)

        try:
            # שחזור מסד הנתונים
            self.restore_database(backup_path)

            # שחזור קבצי מדיה
            self.restore_media(backup_path)

            # הצגת מטא-דאטה
            self.show_metadata(backup_path)

            self.stdout.write(self.style.SUCCESS(f'✅ השחזור הושלם בהצלחה מ-{backup_name}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ שגיאה בשחזור: {str(e)}'))
            raise

    def validate_backup(self, backup_path):
        """בדיקת תקינות גיבוי"""
        required_files = ['db.sqlite3', 'metadata.json']

        for file in required_files:
            file_path = os.path.join(backup_path, file)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'  ❌ חסר קובץ: {file}'))
                return False

        return True

    def restore_database(self, backup_path):
        """שחזור מסד הנתונים"""
        backup_db = os.path.join(backup_path, 'db.sqlite3')
        current_db = settings.DATABASES['default']['NAME']

        if os.path.exists(backup_db):
            # גיבוי המצב הנוכחי למקרה חירום
            if os.path.exists(current_db):
                emergency_backup = f"{current_db}.emergency_backup"
                shutil.copy2(current_db, emergency_backup)

            # שחזור
            shutil.copy2(backup_db, current_db)

            size_mb = os.path.getsize(current_db) / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(f'  ✅ מסד נתונים שוחזר: {size_mb:.2f} MB'))

    def restore_media(self, backup_path):
        """שחזור קבצי מדיה"""
        backup_media = os.path.join(backup_path, 'media')
        current_media = settings.MEDIA_ROOT

        if os.path.exists(backup_media):
            # גיבוי המדיה הנוכחית
            if os.path.exists(current_media):
                emergency_backup = f"{current_media}_emergency_backup"
                if os.path.exists(emergency_backup):
                    shutil.rmtree(emergency_backup)
                shutil.copytree(current_media, emergency_backup)
                shutil.rmtree(current_media)

            # שחזור
            shutil.copytree(backup_media, current_media)

            file_count = sum([len(files) for r, d, files in os.walk(current_media)])
            self.stdout.write(self.style.SUCCESS(f'  ✅ קבצי מדיה שוחזרו: {file_count} קבצים'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  אין קבצי מדיה בגיבוי'))

    def show_metadata(self, backup_path):
        """הצגת מטא-דאטה של הגיבוי"""
        metadata_path = os.path.join(backup_path, 'metadata.json')

        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            self.stdout.write(self.style.SUCCESS('\n📋 פרטי הגיבוי:'))
            self.stdout.write(f"  תאריך: {metadata.get('backup_date', 'לא ידוע')}")
            self.stdout.write(f"  גרסה: {metadata.get('backup_version', 'לא ידוע')}")

    def list_available_backups(self, backup_dir):
        """הצגת גיבויים זמינים"""
        if not os.path.exists(backup_dir):
            self.stdout.write(self.style.WARNING('\n📁 אין גיבויים זמינים'))
            return

        backups = []
        for item in os.listdir(backup_dir):
            item_path = os.path.join(backup_dir, item)
            if os.path.isdir(item_path) and item.startswith('backup_'):
                ctime = os.path.getctime(item_path)
                backups.append((item, datetime.fromtimestamp(ctime)))

        if backups:
            self.stdout.write(self.style.SUCCESS('\n📁 גיבויים זמינים:'))
            backups.sort(key=lambda x: x[1], reverse=True)
            for backup_name, backup_date in backups[:10]:  # מציג 10 האחרונים
                self.stdout.write(f"  • {backup_name} ({backup_date.strftime('%d/%m/%Y %H:%M')})")
        else:
            self.stdout.write(self.style.WARNING('\n📁 אין גיבויים זמינים'))

