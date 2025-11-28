from django.contrib import admin
from .models import GeneticVariant

@admin.register(GeneticVariant)
class GeneticVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "gene", "chromosome", "position", "impact")
    list_filter = ("chromosome", "impact")
    search_fields = ("gene__symbol",)
