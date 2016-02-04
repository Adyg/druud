from django.contrib import admin

from druud.models import (Project, Check, CheckLog, CheckRequestHeader, CheckPayload)

admin.site.register(Project)
admin.site.register(Check)
admin.site.register(CheckLog)
admin.site.register(CheckRequestHeader)
admin.site.register(CheckPayload)
