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

    class Meta:
        verbose_name = _('استراتيجية')
        verbose_name_plural = _('استراتيجيات')
        ordering = ['-created_at']

    def __str__(self):
        return self.title