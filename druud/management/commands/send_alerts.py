from django.core.management.base import BaseCommand, CommandError

from druud.models import AlertLog


class Command(BaseCommand):
    help = 'Send alerts.'

    def handle(self, *args, **options):
        pending_alerts = AlertLog.get_pending_alerts_batch()

        for alert in pending_alerts:
            alert.notify()
