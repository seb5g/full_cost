from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
from .models import Experiment, Record, Extraction


admin.site.register(Experiment, SimpleHistoryAdmin)
admin.site.register(Record, SimpleHistoryAdmin)
