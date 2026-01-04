from django.contrib import admin
from .models import ReportData,Event,VEN

@admin.register(VEN)
class VEN(admin.ModelAdmin):
    pass
@admin.register(ReportData)
class ReportData(admin.ModelAdmin):
    pass

@admin.register(Event)
class Event(admin.ModelAdmin):
    pass