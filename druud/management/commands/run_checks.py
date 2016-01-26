from django.core.management.base import BaseCommand, CommandError

from druud.models import Check


class Command(BaseCommand):
    help = 'Run checks.'

    def handle(self, *args, **options):
        pending_checks = Check.get_pending_checks_batch()

        for check in pending_checks:
            check.perform_check()
