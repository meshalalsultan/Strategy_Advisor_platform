# trading/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import Strategy
from .forms import StrategyForm
from users.decorators import profile_required


class StrategyListView(LoginRequiredMixin, ListView):
    model = Strategy
    template_name = 'trading/strategy_list.html'
    context_object_name = 'strategies'
    paginate_by = 10

    def get_queryset(self):
        return Strategy.objects.filter(user=self.request.user)

class StrategyDetailView(LoginRequiredMixin, DetailView):
    model = Strategy
    template_name = 'trading/strategy_detail.html'
    context_object_name = 'strategy'

    def get_queryset(self):
        return Strategy.objects.filter(user=self.request.user)


@login_required
def strategy_list(request):
    strategies = Strategy.objects.filter(user=request.user)
    return render(request, 'trading/strategy_list.html', {
        'strategies': strategies
    })

@login_required
def generate_strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user
            strategy.save()
            messages.success(request, _('تم إنشاء الاستراتيجية بنجاح!'))
            return redirect('trading:strategy_list')
    else:
        form = StrategyForm()
    
    context = {
        'form': form,
        'title': _('إنشاء استراتيجية جديدة')
    }
    return render(request, 'trading/strategy_form.html', context)
    
@login_required
def toggle_favorite(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk)
    strategy.is_favorite = not strategy.is_favorite
    strategy.save()
    return redirect('trading:strategy_detail', pk=pk)

   
@login_required
def strategy_detail(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    return render(request, 'trading/strategy_detail.html', {
        'strategy': strategy
    })
    
@login_required
def strategy_detail(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    return render(request, 'trading/strategy_detail.html', {
        'strategy': strategy
    })
    
        
@login_required
@profile_required
def generate_strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user
            strategy.save()
            messages.success(request, _('تم إنشاء الاستراتيجية بنجاح!'))
            return redirect('trading:strategy_detail', pk=strategy.pk)
    else:
        form = StrategyForm()
    
    return render(request, 'trading/strategy_form.html', {
        'form': form,
        'title': _('إنشاء استراتيجية جديدة')
    })

@login_required
def update_strategy(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = StrategyForm(request.POST, instance=strategy)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم تحديث الاستراتيجية بنجاح!'))
            return redirect('trading:strategy_detail', pk=strategy.pk)
    else:
        form = StrategyForm(instance=strategy)
    
    return render(request, 'trading/strategy_form.html', {
        'form': form,
        'strategy': strategy,
        'title': _('تعديل الاستراتيجية')
    })

@login_required
def delete_strategy(request, pk):
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    
    if request.method == 'POST':
        strategy.delete()
        messages.success(request, _('تم حذف الاستراتيجية بنجاح!'))
        return redirect('trading:strategy_list')
    
    return render(request, 'trading/strategy_confirm_delete.html', {
        'strategy': strategy,
        'title': _('حذف الاستراتيجية')
    })