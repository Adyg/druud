import uuid as uuid_module

from django.db import models


class Contact(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_module.uuid4, editable=False)
    name = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name
