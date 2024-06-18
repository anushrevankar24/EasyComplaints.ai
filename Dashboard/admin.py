from django.contrib import admin
from .models import Complaint

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Complaint, CustomUserAdmin)
