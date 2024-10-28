from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.simple_tag
def profile_completion_percentage(user):
    """Calculate the profile completion percentage."""
    profile = user.profile
    total_fields = 12  # Total number of profile fields we want to track
    completed_fields = 0
    
    # Required fields
    if profile.name:
        completed_fields += 1
    if profile.experience_level:
        completed_fields += 1
    if profile.trading_style:
        completed_fields += 1
    if profile.risk_management:
        completed_fields += 1
    if profile.favorite_assets:
        completed_fields += 1
    if profile.financial_goals:
        completed_fields += 1
    if profile.trading_hours:
        completed_fields += 1
    if profile.analysis_type:
        completed_fields += 1
    
    # Optional fields
    if profile.avatar:
        completed_fields += 1
    if profile.telegram:
        completed_fields += 1
    if profile.country:
        completed_fields += 1
    if profile.trading_platform:
        completed_fields += 1
    
    return int((completed_fields / total_fields) * 100)

@register.inclusion_tag('users/tags/profile_completion.html')
def show_profile_completion(user):
    """Show profile completion progress bar."""
    percentage = profile_completion_percentage(user)
    return {
        'percentage': percentage,
        'user': user,
    }