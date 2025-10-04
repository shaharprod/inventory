"""
פקודת ניהול לצפייה בלוגים
"""
import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'צפייה וניתוח קבצי לוג'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='general',
            choices=['general', 'errors', 'security', 'database', 'all'],
            help='סוג הלוג לצפייה'
        )
        parser.add_argument(
            '--lines',
            type=int,
            default=50,
            help='מספר שורות אחרונות להצגה'
        )
        parser.add_argument(
            '--search',
            type=str,
            help='חיפוש טקסט בלוג'
        )
        parser.add_argument(
            '--tail',
            action='store_true',
            help='מעקב בזמן אמת אחר הלוג'
        )

    def handle(self, *args, **options):
        log_type = options['type']
        lines_count = options['lines']
        search_term = options['search']
        tail_mode = options['tail']

        logs_dir = settings.LOGS_DIR

        if not os.path.exists(logs_dir):
            self.stdout.write(self.style.WARNING('📁 תיקיית הלוגים לא קיימת'))
            return

        if log_type == 'all':
            log_files = ['general.log', 'errors.log', 'security.log', 'database.log']
        else:
            log_files = [f'{log_type}.log']

        for log_file in log_files:
            log_path = os.path.join(logs_dir, log_file)

            if not os.path.exists(log_path):
                self.stdout.write(self.style.WARNING(f'⚠️  {log_file} לא נמצא'))
                continue

            self.stdout.write(self.style.SUCCESS(f'\n{"="*80}'))
            self.stdout.write(self.style.SUCCESS(f'📄 {log_file}'))
            self.stdout.write(self.style.SUCCESS(f'{"="*80}\n'))

            # קריאת הקובץ
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # סינון לפי חיפוש
            if search_term:
                lines = [line for line in lines if search_term.lower() in line.lower()]
                self.stdout.write(self.style.WARNING(f'🔍 נמצאו {len(lines)} שורות עם "{search_term}"\n'))

            # הצגת שורות אחרונות
            display_lines = lines[-lines_count:] if len(lines) > lines_count else lines

            for line in display_lines:
                # צביעה לפי רמת חומרה
                if '[ERROR]' in line or '[CRITICAL]' in line:
                    self.stdout.write(self.style.ERROR(line.rstrip()))
                elif '[WARNING]' in line:
                    self.stdout.write(self.style.WARNING(line.rstrip()))
                elif '[INFO]' in line:
                    self.stdout.write(line.rstrip())
                else:
                    self.stdout.write(line.rstrip())

            # סטטיסטיקות
            self.show_statistics(lines, log_file)

    def show_statistics(self, lines, log_file):
        """הצגת סטטיסטיקות על הלוג"""
        error_count = sum(1 for line in lines if '[ERROR]' in line)
        warning_count = sum(1 for line in lines if '[WARNING]' in line)
        info_count = sum(1 for line in lines if '[INFO]' in line)

        self.stdout.write(self.style.SUCCESS(f'\n📊 סטטיסטיקות {log_file}:'))
        self.stdout.write(f'   סה"כ שורות: {len(lines)}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'   ❌ שגיאות: {error_count}'))
        if warning_count > 0:
            self.stdout.write(self.style.WARNING(f'   ⚠️  אזהרות: {warning_count}'))
        if info_count > 0:
            self.stdout.write(f'   ℹ️  מידע: {info_count}')

