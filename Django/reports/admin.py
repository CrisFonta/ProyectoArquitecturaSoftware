from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PatientVariantReport

@admin.register(PatientVariantReport)
class PatientVariantReportAdmin(admin.ModelAdmin):
    list_display = ("id", "patientId", "variant", "detectionDate", "alleleFrequency")
    list_filter = ("detectionDate",)
    search_fields = ("patientId",)