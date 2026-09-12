from django.core.management.base import BaseCommand
from core.compile_locales import compile_all_locales


class Command(BaseCommand):
    help = 'Compiles .po message catalogs into valid GNU gettext binary .mo files without requiring external gettext tools.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Compiling all locale message files...'))
        compiled = compile_all_locales()
        self.stdout.write(self.style.SUCCESS(f'Successfully compiled {len(compiled)} locale catalog(s).'))
