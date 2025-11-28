from rest_framework import serializers
from .models import PatientVariantReport

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVariantReport
        fields = "__all__"
