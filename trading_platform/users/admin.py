# users/admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'experience_level', 'trading_style', 'country')
    list_filter = ('experience_level', 'trading_style', 'analysis_type', 'country')

admin.site.register(Profile, ProfileAdmin)
