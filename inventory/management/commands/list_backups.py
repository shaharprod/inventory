"""
פקודת ניהול להצגת רשימת גיבויים
"""
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'הצגת רשימת כל הגיבויים הזמינים'

    def add_arguments(self, parser):
        parser.add_argument(
            '--backup-dir',
            type=str,
            default='backups',
            help='תיקיית הגיבויים'
        )

    def handle(self, *args, **options):
        backup_dir = options['backup_dir']

        if not os.path.exists(backup_dir):
            self.stdout.write(self.style.WARNING('📁 תיקיית הגיבויים לא קיימת'))
            return

        backups = []
        total_size = 0

        for item in os.listdir(backup_dir):
            item_path = os.path.join(backup_dir, item)
            if os.path.isdir(item_path) and item.startswith('backup_'):
                # קריאת מטא-דאטה
                metadata_path = os.path.join(item_path, 'metadata.json')
                metadata = {}
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                # חישוב גודל תיקייה
                size = self.get_dir_size(item_path)
                total_size += size

                backups.append({
                    'name': item,
                    'date': datetime.fromtimestamp(os.path.getctime(item_path)),
                    'size': size,
                    'metadata': metadata
                })

        if not backups:
            self.stdout.write(self.style.WARNING('📁 אין גיבויים זמינים'))
            return

        # מיון לפי תאריך
        backups.sort(key=lambda x: x['date'], reverse=True)

        # הצגת כותרת
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS(f'📦 רשימת גיבויים ({len(backups)} גיבויים זמינים)'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # הצגת גיבויים
        for i, backup in enumerate(backups, 1):
            self.stdout.write(self.style.WARNING(f"{i}. {backup['name']}"))
            self.stdout.write(f"   📅 תאריך: {backup['date'].strftime('%d/%m/%Y %H:%M:%S')}")
            self.stdout.write(f"   💾 גודל: {self.format_size(backup['size'])}")

            if backup['metadata']:
                backup_date = backup['metadata'].get('backup_date', '')
                if backup_date:
                    self.stdout.write(f"   🏷️  מטא-דאטה: {backup_date}")

            self.stdout.write('')

        # סיכום
        self.stdout.write(self.style.SUCCESS('='*80))
        self.stdout.write(f"📊 סה\"כ גיבויים: {len(backups)}")
        self.stdout.write(f"💾 סה\"כ נפח: {self.format_size(total_size)}")
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # הוראות שחזור
        self.stdout.write(self.style.WARNING('📝 לשחזור גיבוי, הרץ:'))
        if backups:
            self.stdout.write(f"   python manage.py restore_database {backups[0]['name']}\n")

    def get_dir_size(self, path):
        """חישוב גודל תיקייה"""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total += os.path.getsize(filepath)
        return total

    def format_size(self, size_bytes):
        """פורמט גודל קובץ"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

