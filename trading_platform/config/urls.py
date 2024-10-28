# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # استخدام TemplateView مباشرة للصفحة الرئيسية
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # تضمين URLs من التطبيقات
    path('users/', include('users.urls')),
    path('trading/', include('trading.urls')),
    path('blog/', include('blog.urls')),
    path('rewards/', include('rewards.urls')),
    path('accounts/', include('allauth.urls')),
]

# إضافة مسارات الميديا والملفات الثابتة في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)