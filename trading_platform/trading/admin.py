
# Register your models here.
from django.contrib import admin
from .models import Strategy

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # قم بتعديل الحقول حسب الحاجة
    search_fields = ('title', 'user__username')
