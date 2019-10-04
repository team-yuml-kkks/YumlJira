from django.contrib import admin

from .models import *


admin.site.register(Task)
admin.site.register(Project)
admin.site.register(TimeLog)
admin.site.register(Column)
admin.site.register(Sprint)

