# rewards/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from .models import Points, Reward

@login_required
def dashboard(request):
    total_points = Points.objects.filter(user=request.user).aggregate(
        total=Sum('points')
    )['total'] or 0
    
    recent_points = Points.objects.filter(user=request.user)[:5]
    available_rewards = Reward.objects.filter(
        is_active=True,
        points_required__lte=total_points
    )

    context = {
        'total_points': total_points,
        'recent_points': recent_points,
        'available_rewards': available_rewards,
    }
    return render(request, 'rewards/dashboard.html', context)

@login_required
def points_history(request):
    points_list = Points.objects.filter(user=request.user)
    total_points = points_list.aggregate(total=Sum('points'))['total'] or 0
    
    context = {
        'points_list': points_list,
        'total_points': total_points,
    }
    return render(request, 'rewards/points_history.html', context)

@login_required
def available_rewards(request):
    total_points = Points.objects.filter(user=request.user).aggregate(
        total=Sum('points')
    )['total'] or 0
    
    rewards_list = Reward.objects.filter(is_active=True)
    
    context = {
        'rewards_list': rewards_list,
        'total_points': total_points,
    }
    return render(request, 'rewards/available_rewards.html', context)

@login_required
def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id, is_active=True)
    total_points = Points.objects.filter(user=request.user).aggregate(
        total=Sum('points')
    )['total'] or 0
    
    if total_points < reward.points_required:
        messages.error(request, _('عدد النقاط غير كافٍ لاسترداد هذه المكافأة.'))
        return redirect('rewards:available_rewards')
    
    Points.objects.create(
        user=request.user,
        points=-reward.points_required,
        reason=f"استرداد مكافأة: {reward.title}"
    )
    
    messages.success(request, _('تم استرداد المكافأة بنجاح!'))
    return redirect('rewards:dashboard')