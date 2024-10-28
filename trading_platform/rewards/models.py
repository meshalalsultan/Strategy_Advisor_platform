# rewards/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Points(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('المستخدم')
    )
    points = models.IntegerField(_('النقاط'))
    reason = models.CharField(_('السبب'), max_length=255)
    date = models.DateTimeField(_('التاريخ'), auto_now_add=True)

    class Meta:
        verbose_name = _('نقطة')
        verbose_name_plural = _('نقاط')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.email}: {self.points} نقاط"

class Reward(models.Model):
    title = models.CharField(_('العنوان'), max_length=255)
    description = models.TextField(_('الوصف'))
    points_required = models.IntegerField(_('النقاط المطلوبة'))
    is_active = models.BooleanField(_('نشط'), default=True)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)

    class Meta:
        verbose_name = _('مكافأة')
        verbose_name_plural = _('مكافآت')
        ordering = ['points_required']

    def __str__(self):
        return f"{self.title} ({self.points_required} نقطة)"