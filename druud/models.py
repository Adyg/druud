import uuid as uuid_module
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings

from druud.browser import DruudBrowser
from alerting.models import Contact


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_module.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.TextField(blank=False, null=False)

    def __unicode__(self):

        return '%s' % self.name


class Check(models.Model):
    check_types = (
        ('H', 'HEAD'),
        ('G', 'GET'),
        ('P', 'POST'),
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
    name = models.TextField(blank=False, null=False)
    project = models.ForeignKey(Project)
    address = models.TextField(blank=False, null=False)
    check_type = models.CharField(db_index=True, max_length=1, choices=check_types, blank=False, null=False)
    check_frequency = models.CharField(db_index=True, max_length=3, choices=check_frequency, blank=False, null=False)
    check_status = models.CharField(db_index=True, max_length=1, choices=check_status, blank=False, null=False, default='P')
    next_check = models.DateTimeField(default=timezone.now)
    port = models.IntegerField(blank=True, null=True)
    http_auth_username = models.TextField(blank=True, null=True)
    http_auth_password = models.TextField(blank=True, null=True)
    contact = models.ManyToManyField(Contact)

    def __unicode__(self):

        return '%s - %s/%s' % (self.project, self.check_type, self.check_frequency)

    def perform_check(self):
        check_result = False

        if self.check_type == 'H':
            check_result = self._head_check()
        elif self.check_type == 'G':
            check_result = self._get_check()
        elif self.check_type == 'P':
            check_result = self._post_check()

        self.mark_checked()
        CheckLog.create(self, check_result)

    def to_browser_config(self):
        browser_config_dict = {
            'url': self.address,
            'port': self.port,
            'http_auth_username': self.http_auth_username,
            'http_auth_password': self.http_auth_password,
            'headers': self.get_headers_dict(),
            'payload': self.get_payload_dict(),
            'payload_files': {},
        }

        if self.check_type == 'P':
            browser_config_dict['payload_files'] = self.get_payload_files_dict()

        return browser_config_dict

    def get_browser(self):

        return DruudBrowser(self.to_browser_config())

    def _head_check(self):
        browser = self.get_browser()

        check_result = browser.head_request()

        return check_result

    def _get_check(self):
        browser = self.get_browser()

        check_result = browser.get_request()

        return check_result

    def _post_check(self):
        browser = self.get_browser()

        check_result = browser.post_request()

        return check_result

    def mark_checked(self):
        self.check_status = 'P'
        self.next_check = timezone.now() + timedelta(minutes=int(self.check_frequency))
        self.save()

        return self

    def get_headers_dict(self):
        headers_dict = {}

        headers = self.checkrequestheader_set.all()
        for header in headers:
            headers_dict[header.header_key] = header.header_value

        return headers_dict

    def get_payload_dict(self):
        payload_dict = {}

        payload_elements = self.checkpayload_set.filter(pfile__isnull=True)

        for payload_element in payload_elements:
            payload_dict[payload_element.key] = payload_element.value

        return payload_dict

    def get_payload_files_dict(self):
        payload_files_dict = {}

        payload_elements = self.checkpayload_set.exclude(pfile__isnull=True).exclude(pfile='')

        for payload_element in payload_elements:
            payload_files_dict[payload_element.key] = payload_element.pfile

        return payload_files_dict

    @classmethod
    def get_pending_checks_batch(cls, batch_size=False):
        if not batch_size:
            batch_size = settings.DRUUD_CHECK_BATCH_SIZE

        # checks that are not currently running
        #batch = cls.objects.filter(check_status='P')

        # checks that are past their due check date
        #batch = batch.filter(next_check__lte=timezone.now())

        batch = cls.objects.all()
        batch = batch[:batch_size]

        # mark the batch as running so other tasks don't pick it up
        for check in batch:
            check.check_status = 'R'
            check.save()

        return batch


class CheckRequestHeader(models.Model):
    related_check = models.ForeignKey(Check)
    header_key = models.TextField(blank=False, null=False)
    header_value = models.TextField(blank=True, null=True)


def payload_directory(instance, filename):
    path_parts = ['payloads', str(instance.related_check.project.pk), str(instance.related_check.pk), str(instance.pk), filename]

    return '/'.join(path_parts)


class CheckPayload(models.Model):
    related_check = models.ForeignKey(Check)
    key = models.TextField(blank=False, null=False)
    value = models.TextField(blank=True, null=True)
    pfile = models.FileField(upload_to=payload_directory, blank=True, null=True)


class CheckLog(models.Model):
    related_check = models.ForeignKey(Check)
    result = models.IntegerField()
    status = models.TextField()
    elapsed = models.FloatField()
    check_date = models.DateTimeField(default=timezone.now)
    error = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    @classmethod
    def create(cls, check, check_result):
        check_log = CheckLog.objects.create(
            related_check=check,
            result=int(check_result['status']),
            status=check_result['status_code'],
            elapsed=check_result['elapsed'],
            error=check_result['error'],
            error_message=check_result['error_message'],
        )

        if check_log.is_alerting():
            AlertLog.create(check_log)

    def is_alerting(self):
        if int(self.status) >= 400:

            return True

        return False


class AlertLog(models.Model):
    ALERT_STATUSES = (
        ('P', 'Pending'),
        ('S', 'Sent'),
        ('F', 'Failed'),
    )

    related_check = models.ForeignKey(Check)
    related_contact = models.ForeignKey(Contact)
    alert_message = models.TextField(blank=False, null=False, default='')
    alert_status = models.CharField(max_length=1, choices=ALERT_STATUSES, blank=True, null=True, default='P')

    @classmethod
    def create(cls, check_log):
        alert_message = AlertLog.build_alert_message(check_log)

        for contact in check_log.related_check.contact.all():
            AlertLog.objects.create(
                related_check=check_log.related_check,
                related_contact=contact,
                alert_message=alert_message
            )

    @classmethod
    def build_alert_message(cls, check_log):

        return '%s seems to be down. Please check.' % (check_log.related_check.project.name)

    @classmethod
    def get_pending_alerts_batch(cls):

        return cls.objects.filter(alert_status='P')

    def notify(self):
        self.related_contact.notify(self)

        self.alert_status = 'S'
        self.save()
