from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Gene

@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "fullName")
    search_fields = ("symbol", "fullName")
