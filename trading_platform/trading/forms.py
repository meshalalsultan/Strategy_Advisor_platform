# trading/forms.py
from django import forms
from .models import Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['title', 'content']
        labels = {
            'title': 'عنوان الاستراتيجية',
            'content': 'محتوى الاستراتيجية'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'اكتب محتوى الاستراتيجية هنا...'
            })
        }