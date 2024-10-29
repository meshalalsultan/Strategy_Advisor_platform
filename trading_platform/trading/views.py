# trading/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import Strategy
from .forms import StrategyForm
from users.decorators import profile_required
from django.http import HttpResponseRedirect
from .utils import TradingStrategyGenerator
from django.contrib.auth.models import User
from django.urls import reverse
import logging

# إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)




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

def strategy_summary_view(request):
    strategy_data = request.session.get('strategy_data')
    if not strategy_data:
        return redirect('trading:create_strategy')  # في حالة عدم وجود بيانات، إعادة التوجيه

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            form = StrategyForm(strategy_data)
            if form.is_valid():
                strategy = form.save(commit=False)
                strategy.user = request.user
                strategy.save()
                messages.success(request, "تم إنشاء الاستراتيجية بنجاح.")
                return redirect('trading:strategy_list')
        else:
            return redirect('trading:create_strategy')

    return render(request, 'trading/strategy_summary.html', {'strategy_data': strategy_data})

    strategy_data = request.session.get('strategy_data')
    if not strategy_data:
        return redirect('trading:generate_strategy')  # في حالة عدم وجود بيانات، إعادة التوجيه

    if request.method == 'POST':
        # إذا تم تأكيد الاستراتيجية، احفظها في قاعدة البيانات
        if request.POST.get('confirm') == 'yes':
            form = StrategyForm(strategy_data)
            if form.is_valid():
                strategy = form.save(commit=False)
                strategy.user = request.user
                strategy.save()
                messages.success(request, "تم إنشاء الاستراتيجية بنجاح.")
                return redirect('trading:strategy_list')
        else:
            return redirect('trading:generate_strategy')

    return render(request, 'trading/strategy_summary.html', {'strategy_data': strategy_data})


def user_strategies_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    strategies = Strategy.objects.filter(user=user)

    return render(request, 'user_strategies.html', {
        'user': user,
        'strategies': strategies,
    })
def confirm_strategy_view(request):
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            strategy_data = request.session.get('strategy_data')
            if strategy_data:
                form = StrategyForm(strategy_data)
                if form.is_valid():
                    form.save()
                    messages.success(request, "تم إنشاء الاستراتيجية بنجاح.")
                    return redirect('user_strategies')
        else:
            return redirect('create_strategy')
    return redirect('create_strategy')


def create_strategy_view(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            # تخزين البيانات في الجلسة لدعم العرض العربي في الملخص
            request.session['strategy_data'] = form.cleaned_data
            return redirect('trading:strategy_summary')
        else:
            messages.error(request, "حدث خطأ أثناء إنشاء الاستراتيجية. يرجى التأكد من المدخلات.")
    else:
        form = StrategyForm()

    return render(request, 'trading/strategy_form.html', {'form': form})
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الاستراتيجية بنجاح.")
            return redirect('user_strategies')  # يعيد التوجيه لعرض الاستراتيجيات
        else:
            messages.error(request, "حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى.")
    else:
        form = StrategyForm()
    
    return render(request, 'create_strategy.html', {'form': form})



    
@login_required
def strategy_list(request):
    strategies = Strategy.objects.filter(user=request.user)
    return render(request, 'trading/strategy_list.html', {
        'strategies': strategies
    })


@login_required
@profile_required

def generate_strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user
            try:
                # إعداد prompt وإرسال الطلب لـ ChatGPT
                user_profile = request.user.profile
                strategy_generator = TradingStrategyGenerator()
                generated_content = strategy_generator.generate_strategy(user_profile)
                strategy.content = generated_content
                request.session['strategy_data'] = {
                    'title': strategy.title,
                    'content': strategy.content,
                    'experience_level': strategy.experience_level,
                    'trading_style': strategy.trading_style,
                    'risk_management': strategy.risk_management,
                    'preferred_assets': strategy.preferred_assets,
                    'financial_goals': strategy.financial_goals,
                    'trading_hours': strategy.trading_hours,
                    'market_analysis': strategy.market_analysis,
                }
                return redirect('trading:strategy_summary')
            except Exception as e:
                messages.error(request, f"حدث خطأ أثناء إنشاء الاستراتيجية. التفاصيل: {str(e)}")
                return redirect('trading:generate_strategy')
    else:
        form = StrategyForm()
    return render(request, 'trading/strategy_form.html', {'form': form})
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user

            try:
                # طباعة بيانات الملف الشخصي للتحقق
                user_profile = request.user.profile
                logger.info("User Profile: %s", user_profile)

                # التحقق من استدعاء TradingStrategyGenerator
                strategy_generator = TradingStrategyGenerator()
                logger.info("Calling TradingStrategyGenerator for user profile %s", user_profile)

                generated_content = strategy_generator.generate_strategy(user_profile)
                logger.info("Generated Content: %s", generated_content)

                strategy.content = generated_content
                request.session['strategy_data'] = {
                    'title': strategy.title,
                    'content': strategy.content,
                    'experience_level': strategy.experience_level,
                    'trading_style': strategy.trading_style,
                    'risk_management': strategy.risk_management,
                    'preferred_assets': strategy.preferred_assets,
                    'financial_goals': strategy.financial_goals,
                    'trading_hours': strategy.trading_hours,
                    'market_analysis': strategy.market_analysis,
                }
                return redirect('trading:strategy_summary')
            except Exception as e:
                logger.error("Error generating strategy: %s", str(e))
                messages.error(request, f"حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى. التفاصيل: {str(e)}")
                return redirect('trading:generate_strategy')
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
