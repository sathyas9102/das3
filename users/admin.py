from django.contrib import admin
from .models import Department, CustomUser, DailyActivityReport

admin.site.register(Department)
admin.site.register(CustomUser)
admin.site.register(DailyActivityReport)
