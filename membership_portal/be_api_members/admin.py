from django.contrib import admin
from .models import Country, Organization

# Register your models here.
admin.site.register(Country)
admin.site.register(Organization)