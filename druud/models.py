import uuid as uuid_module
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone
from django.conf import settings


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_module.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.TextField(blank=False, null=False)

    def __unicode__(self):

        return '%s' % self.name


class Check(models.Model):
    check_types = (
            ('A', 'Alive'),
        )

    # in seconds
    check_frequency = (
            ('5', '5min'),
            ('10', '10min'),
        )

    check_status = (
            ('P', 'Pending'),
            ('R', 'Running'),
        )

    uuid = models.UUIDField(primary_key=True, default=uuid_module.uuid4, editable=False)
    project = models.ForeignKey(Project)
    address = models.TextField(blank=False, null=False)
    check_type = models.CharField(db_index=True, max_length=1, choices=check_types, blank=False, null=False)
    check_frequency = models.CharField(db_index=True, max_length=3, choices=check_frequency, blank=False, null=False)
    check_status = models.CharField(db_index=True, max_length=1, choices=check_status, blank=False, null=False, default='P')
    next_check = models.DateTimeField(default=timezone.now)

    def __unicode__(self):

        return '%s - %s/%s' % (self.project, self.check_type, self.check_frequency)

    def perform_check(self):

        if self.check_type == 'A':
            self._alive_check()

    def _alive_check(self):


        self.mark_checked()

        return True

    def mark_checked(self):
        self.check_status = 'P'
        self.next_check = timezone.now() + timedelta(minutes=int(self.check_frequency))
        self.save()

        return self

    @classmethod
    def get_pending_checks_batch(cls, batch_size=False):
        if not batch_size:
            batch_size = settings.DRUUD_CHECK_BATCH_SIZE

        # checks that are not currently running
        batch = cls.objects.filter(check_status='P')

        # checks that are past their due check date
        batch = batch.filter(next_check__lte=timezone.now())

        batch = batch[:batch_size]

        # mark the batch as running so other tasks don't pick it up
        for check in batch:
            check.check_status = 'R'
            check.save()

        return batch


class CheckLog(models.Model):
    related_check = models.ForeignKey(Check)
    results = models.TextField()
