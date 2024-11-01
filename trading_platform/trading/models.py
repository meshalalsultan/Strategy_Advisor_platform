from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Strategy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('المستخدم')
    )
    title = models.CharField(_('العنوان'), max_length=255)
    content = models.TextField(_('المحتوى'))
    is_favorite = models.BooleanField(_('مفضلة'), default=False)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    # الحقول الجديدة
    experience_level = models.CharField(
        _('مستوى الخبرة'),
        max_length=50,
        choices=[('beginner', 'مبتدئ'), ('intermediate', 'متوسط'), ('advanced', 'متقدم')],
        default='beginner'
    )

    trading_style = models.CharField(
        _('أسلوب التداول'),
        max_length=50,
        choices=[('day', 'تداول يومي'), ('swing', 'تداول السوينغ'), ('long', 'استثمار طويل الأمد')],
        default='day'
    )

    risk_management = models.DecimalField(
        _('إدارة المخاطر'),
        max_digits=5,
        decimal_places=2,
        default=1.00,
        help_text="نسبة المخاطرة بالنسبة لرأس المال."
    )

    preferred_assets = models.CharField(
        _('الأصول المفضلة'),
        max_length=255,
        default='Forex',
        help_text="مثل الفوركس، الأسهم، أو العملات الرقمية."
    )

    financial_goals = models.CharField(
        _('الأهداف المالية'),
        max_length=255,
        default='Monthly profit target',
        help_text="الهدف المالي اليومي أو الأسبوعي أو الشهري."
    )

    trading_hours = models.CharField(
        _('ساعات التداول'),
        max_length=255,
        default='9am-5pm',
        help_text="أوقات التداول المفضلة."
    )

    market_analysis = models.CharField(
        _('تحليل السوق المفضل'),
        max_length=50,
        choices=[('technical', 'التحليل الفني'), ('fundamental', 'التحليل الأساسي'), ('mixed', 'مزيج بينهما')],
        default='technical'
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    chatgpt_response = models.TextField(blank=True, null=True)  # حقل لتخزين رد ChatGPT
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('استراتيجية')
        verbose_name_plural = _('استراتيجيات')
        ordering = ['-created_at']

    def __str__(self):
        return self.title
