from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Exclude certain paths from the check
            excluded_paths = [
                reverse('users:profile'),
                reverse('account_logout'),
                '/admin/',
            ]
            
            if not any(request.path.startswith(path) for path in excluded_paths):
                profile = request.user.profile
                # Check if required fields are completed
                required_fields = [
                    'name',
                    'experience_level',
                    'trading_style',
                    'risk_management',
                    'favorite_assets',
                    'financial_goals',
                    'trading_hours',
                    'analysis_type',
                ]
                
                incomplete_fields = [field for field in required_fields 
                                  if not getattr(profile, field)]
                
                if incomplete_fields:
                    messages.warning(
                        request,
                        _('يرجى إكمال ملفك الشخصي للوصول إلى جميع الميزات.')
                    )
                    return redirect('users:profile')

        response = self.get_response(request)
        return response