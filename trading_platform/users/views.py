# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .forms import PreRegistrationForm, CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from django.contrib import messages
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.db.models import Sum
from .forms import ProfileUpdateForm
from .forms import ProfileUpdateForm, PreRegistrationForm



def pre_registration(request):
    if request.method == 'POST':
        form = PreRegistrationForm(request.POST)
        if form.is_valid():
            # حفظ البيانات في الجلسة
            request.session['pre_registration_data'] = {
                'experience_level': form.cleaned_data['experience_level'],
                'trading_style': form.cleaned_data['trading_style'],
                'risk_management': form.cleaned_data['risk_management'],
                'favorite_assets': form.cleaned_data['favorite_assets'],
                'financial_goals': form.cleaned_data['financial_goals'],
                'trading_hours': form.cleaned_data['trading_hours'],
                'analysis_type': form.cleaned_data['analysis_type'],
                'age': form.cleaned_data['age'],
                'telegram': form.cleaned_data['telegram'],
                'country': form.cleaned_data['country'],
                'trading_platform': form.cleaned_data['trading_platform'],
                'is_agency_member': form.cleaned_data.get('is_agency_member', False),
                'ai_knowledge': form.cleaned_data.get('ai_knowledge', False),
            }
            return redirect('account_signup')
    else:
        form = PreRegistrationForm()

    return render(request, 'users/pre_registration.html', {
        'form': form,
        'title': _('معلومات التداول')
    })
# دالة التسجيل
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Get pre-registration data from session
            pre_registration_data = request.session.get('pre_registration_data', {})
            
            # Update user profile
            profile = user.profile
            for key, value in pre_registration_data.items():
                setattr(profile, key, value)
            profile.save()
            
            # Clear session data
            del request.session['pre_registration_data']
            
            messages.success(request, _('تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.'))
            return redirect('account_login')
    else:
        if not request.session.get('pre_registration_data'):
            messages.warning(request, _('يرجى إكمال معلومات التداول أولاً.'))
            return redirect('users:pre_registration')
        form = CustomUserCreationForm()

    return render(request, 'account/signup.html', {
        'form': form,
        'title': _('إنشاء حساب')
    })

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Retrieve and use pre-registration data to create Profile
            pre_registration_data = request.session.pop('pre_registration_data', None)
            if pre_registration_data:
                Profile.objects.create(user=user, **pre_registration_data)

            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@receiver(email_confirmed)
def update_user_profile(request, email_address, **kwargs):
    """Update user profile when email is confirmed."""
    user = email_address.user
    pre_reg_data = request.session.get('pre_registration_data', {})
    
    if pre_reg_data:
        profile = user.profile
        for key, value in pre_reg_data.items():
            setattr(profile, key, value)
        profile.save()
        
        # Clear session data
        del request.session['pre_registration_data']

# دالة عرض الملف الشخصي
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث ملفك الشخصي بنجاح!'))
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    # حساب مجموع النقاط
    total_points = request.user.points_set.aggregate(
        total=Sum('points')
    ).get('total', 0) or 0

    context = {
        'form': form,
        'total_points': total_points,
        'title': _('الملف الشخصي')
    }
    return render(request, 'users/profile.html', context)