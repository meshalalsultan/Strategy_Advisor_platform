# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

class PreRegistrationForm(forms.Form):
    EXPERIENCE_LEVELS = [
        ('beginner', _('مبتدئ')),
        ('intermediate', _('متوسط')),
        ('advanced', _('متقدم')),
        ('professional', _('محترف')),
    ]
    
    TRADING_STYLES = [
        ('day', _('تداول يومي')),
        ('swing', _('تداول متأرجح')),
        ('position', _('تداول مركزي')),
        ('scalping', _('مضاربة سريعة')),
    ]
    
    ANALYSIS_TYPES = [
        ('technical', _('تحليل فني')),
        ('fundamental', _('تحليل أساسي')),
        ('both', _('كلاهما')),
    ]

    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_LEVELS,
        label=_('مستوى الخبرة'),
        widget=forms.RadioSelect
    )
    trading_style = forms.ChoiceField(
        choices=TRADING_STYLES,
        label=_('أسلوب التداول'),
        widget=forms.RadioSelect
    )
    risk_management = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('إدارة المخاطر')
    )
    favorite_assets = forms.CharField(
        max_length=255,
        label=_('الأصول المفضلة')
    )
    financial_goals = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('الأهداف المالية')
    )
    trading_hours = forms.CharField(
        max_length=255,
        label=_('ساعات التداول')
    )
    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_TYPES,
        label=_('نوع التحليل المفضل'),
        widget=forms.RadioSelect
    )

    # Optional fields
    age = forms.IntegerField(
        required=False,
        label=_('العمر')
    )
    telegram = forms.CharField(
        max_length=255,
        required=False,
        label=_('حساب التليجرام')
    )
    country = forms.CharField(
        max_length=255,
        required=False,
        label=_('الدولة')
    )
    trading_platform = forms.CharField(
        max_length=255,
        required=False,
        label=_('منصة التداول')
    )
    is_agency_member = forms.BooleanField(
        required=False,
        label=_('مشترك في الوكالة')
    )
    ai_knowledge = forms.BooleanField(
        required=False,
        label=_('لدي معرفة بالذكاء الاصطناعي')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.RadioSelect, forms.CheckboxInput)):
                field.widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'created_at', 'updated_at')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'is_agency_member': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ai_knowledge': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.RadioSelect, forms.CheckboxInput)):
                field.widget.attrs.update({'class': 'form-control'})