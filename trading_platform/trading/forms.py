from django import forms
from .models import Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = [
            'title', 'content', 'experience_level', 'trading_style', 
            'risk_management', 'preferred_assets', 'financial_goals', 
            'trading_hours', 'market_analysis'
        ]
        labels = {
            'title': 'عنوان الاستراتيجية',
            'content': 'محتوى الاستراتيجية',
            'experience_level': 'مستوى الخبرة',
            'trading_style': 'أسلوب التداول',
            'risk_management': 'إدارة المخاطر',
            'preferred_assets': 'الأصول المفضلة',
            'financial_goals': 'الأهداف المالية',
            'trading_hours': 'ساعات التداول',
            'market_analysis': 'تحليل السوق المفضل'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'اكتب محتوى الاستراتيجية هنا...'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'trading_style': forms.Select(attrs={'class': 'form-control'}),
            'risk_management': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'preferred_assets': forms.TextInput(attrs={'class': 'form-control'}),
            'financial_goals': forms.TextInput(attrs={'class': 'form-control'}),
            'trading_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'market_analysis': forms.Select(attrs={'class': 'form-control'})
        }
