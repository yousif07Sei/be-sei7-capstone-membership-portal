from django.contrib import admin
from .models import Country, Organization,Profile,Plan

# Modify fields in admin panel
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'listed']
    search_fields = ["name"]
    search_help_text = 'Search by Country Name'

# Register your models here.

admin.site.register(Country, CountryAdmin)
admin.site.register(Organization)
admin.site.register(Profile)
admin.site.register(Plan)
