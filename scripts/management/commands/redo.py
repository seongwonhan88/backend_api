from django.core.management import call_command, base
import os


class Command(base.BaseCommand):
    help = 'Reset DB and startover with loadded fixtured'

    def handle(self, *args, **options):
        os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
        print("Deleted all migration files.")
        call_command('reset_db', interactive=False)
        call_command('makemigrations')
        call_command('migrate')
