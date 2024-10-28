# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
        help_text=_('Specific permissions for this user.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
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

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    name = models.CharField(_('الاسم'), max_length=255, blank=True)
    experience_level = models.CharField(
        _('مستوى الخبرة'),
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        null=True,
        blank=True
    )
    trading_style = models.CharField(
        _('أسلوب التداول'),
        max_length=20,
        choices=TRADING_STYLES,
        null=True,
        blank=True
    )
    risk_management = models.TextField(_('إدارة المخاطر'), null=True, blank=True)
    favorite_assets = models.CharField(_('الأصول المفضلة'), max_length=255, null=True, blank=True)
    financial_goals = models.TextField(_('الأهداف المالية'), null=True, blank=True)
    trading_hours = models.CharField(_('ساعات التداول'), max_length=255, null=True, blank=True)
    analysis_type = models.CharField(
        _('نوع التحليل المفضل'),
        max_length=20,
        choices=ANALYSIS_TYPES,
        null=True,
        blank=True
    )
    
    # Optional fields
    age = models.IntegerField(_('العمر'), null=True, blank=True)
    telegram = models.CharField(_('تليجرام'), max_length=255, blank=True)
    country = models.CharField(_('الدولة'), max_length=255, blank=True)
    trading_platform = models.CharField(_('منصة التداول'), max_length=255, blank=True)
    is_agency_member = models.BooleanField(_('مشترك في الوكالة'), default=False)
    ai_knowledge = models.BooleanField(_('معرفة بالذكاء الاصطناعي'), default=False)
    
    avatar = models.ImageField(_('الصورة الشخصية'), upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s profile"