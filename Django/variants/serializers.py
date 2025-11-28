from rest_framework import serializers
from .models import GeneticVariant

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneticVariant
        fields = "__all__"
