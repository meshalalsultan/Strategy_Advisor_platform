from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

def profile_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.profile
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
                    _('يرجى إكمال ملفك الشخصي للوصول إلى هذه الميزة.')
                )
                return redirect('users:profile')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
