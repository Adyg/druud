from django.contrib import admin

from druud.models import (Project, Check, CheckLog)

admin.site.register(Project)
admin.site.register(Check)
admin.site.register(CheckLog)
