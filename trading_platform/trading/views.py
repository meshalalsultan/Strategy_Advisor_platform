# trading/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import TradingStrategyGenerator
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Strategy
from .forms import StrategyForm
from openai import OpenAI


import logging
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect



# إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
def create_strategy_view(request):
    """عرض إنشاء الاستراتيجية الأولية."""
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            # تخزين البيانات في الجلسة لعرضها في ملخص الاستراتيجية
            request.session['strategy_data'] = form.cleaned_data
            return redirect('trading:strategy_summary')  # إعادة التوجيه إلى ملخص الاستراتيجية
        else:
            messages.error(request, "حدث خطأ أثناء إنشاء الاستراتيجية. يرجى التأكد من المدخلات.")
    else:
        form = StrategyForm()
    return render(request, 'trading/strategy_form.html', {'form': form})

@login_required
def user_strategies_view(request, user_id):
    """عرض استراتيجيات مستخدم معين."""
    user = get_object_or_404(User, id=user_id)
    strategies = Strategy.objects.filter(user=user)

    return render(request, 'trading/user_strategies.html', {
        'user': user,
        'strategies': strategies,
    })

@login_required
def confirm_strategy_view(request):
    """تأكيد الاستراتيجية وحفظها بعد موافقة المستخدم."""
    strategy_data = request.session.get('strategy_data')
    if not strategy_data:
        return redirect('trading:create_strategy')  # إعادة التوجيه إذا لم توجد بيانات الاستراتيجية

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':  # في حالة تأكيد الاستراتيجية
            form = StrategyForm(strategy_data)
            if form.is_valid():
                strategy = form.save(commit=False)
                strategy.user = request.user
                strategy.save()
                messages.success(request, "تم تأكيد الاستراتيجية وحفظها بنجاح.")
                return redirect('trading:strategy_list')
            else:
                messages.error(request, "حدث خطأ أثناء تأكيد الاستراتيجية.")
                return redirect('trading:strategy_summary')
        else:
            return redirect('trading:create_strategy')  # إذا اختار تعديل، العودة إلى صفحة الإنشاء

    return redirect('trading:strategy_summary')    

@login_required
def delete_strategy(request, pk):
    """حذف الاستراتيجية المحددة."""
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)

    if request.method == 'POST':
        strategy.delete()
        messages.success(request, "تم حذف الاستراتيجية بنجاح!")
        return redirect('trading:strategy_list')

    return render(request, 'trading/strategy_confirm_delete.html', {
        'strategy': strategy
    })    

@login_required
def toggle_favorite(request, pk):
    """تبديل حالة التفضيل لاستراتيجية معينة."""
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    strategy.is_favorite = not strategy.is_favorite  # تغيير حالة التفضيل
    strategy.save()
    return redirect('trading:strategy_detail', pk=pk) 


@login_required
def strategy_summary_view(request):
    """عرض ملخص الاستراتيجية مع خيارات الموافقة أو التعديل."""
    strategy_data = request.session.get('strategy_data')
    if not strategy_data:
        return redirect('trading:create_strategy')  # في حالة عدم وجود بيانات، إعادة التوجيه

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':  # في حال تم التأكيد
            form = StrategyForm(strategy_data)
            if form.is_valid():
                strategy = form.save(commit=False)
                strategy.user = request.user
                try:
                    # إنشاء المحتوى باستخدام TradingStrategyGenerator
                    strategy_generator = TradingStrategyGenerator()
                    strategy_content = strategy_generator.generate_strategy(request.user.profile)
                    strategy.content = strategy_content
                    strategy.save()
                    messages.success(request, "تم إنشاء الاستراتيجية وحفظها بنجاح.")
                    return redirect('trading:strategy_detail', pk=strategy.pk)
                except Exception as e:
                    logger.error("Error generating strategy with OpenAI: %s", str(e))
                    messages.error(request, f"حدث خطأ أثناء إنشاء الاستراتيجية: {str(e)}")
                    return redirect('trading:strategy_summary')
        else:
            return redirect('trading:create_strategy')  # إعادة التوجيه إلى الإنشاء في حال التعديل

    return render(request, 'trading/strategy_summary.html', {'strategy_data': strategy_data})

@login_required
def strategy_detail(request, pk):
    """عرض تفاصيل الاستراتيجية مع الرد من ChatGPT."""
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    return render(request, 'trading/strategy_detail.html', {
        'strategy': strategy
    })

@login_required
def update_strategy(request, pk):
    """تحديث الاستراتيجية الحالية."""
    strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StrategyForm(request.POST, instance=strategy)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الاستراتيجية بنجاح!")
            return redirect('trading:strategy_detail', pk=strategy.pk)
    else:
        form = StrategyForm(instance=strategy)
    return render(request, 'trading/strategy_form.html', {'form': form, 'strategy': strategy})

@login_required
def generate_strategy(request):
    """دالة لإنشاء الاستراتيجية."""
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": strategy.content}],
                    temperature=0.7,
                    max_tokens=2000
                )
                strategy.chatgpt_response = response.choices[0].message.content
                strategy.save()  # حفظ الاستراتيجية والرد من ChatGPT في قاعدة البيانات
                messages.success(request, "تم إنشاء الاستراتيجية وحفظ رد ChatGPT بنجاح.")
                return redirect('trading:strategy_detail', pk=strategy.pk)
            except Exception as e:
                logger.error("Error generating strategy: %s", str(e))
                messages.error(request, f"حدث خطأ أثناء إنشاء الاستراتيجية. التفاصيل: {str(e)}")
                return redirect('trading:generate_strategy')
        else:
            messages.error(request, "حدث خطأ أثناء معالجة البيانات. تأكد من المدخلات.")
    else:
        form = StrategyForm()
    return render(request, 'trading/strategy_form.html', {'form': form})

@login_required
def generate_strategy(request):
    """توليد استراتيجية باستخدام TradingStrategyGenerator وحفظها."""
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
                strategy.save()
                messages.success(request, "تم توليد الاستراتيجية بنجاح!")
                return redirect('trading:strategy_detail', pk=strategy.pk)
            except Exception as e:
                logger.error(f"Error generating strategy: {str(e)}")
                messages.error(request, f"حدث خطأ أثناء إنشاء الاستراتيجية: {str(e)}")
                return redirect('trading:generate_strategy')
    else:
        form = StrategyForm()
    return render(request, 'trading/strategy_form.html', {'form': form})
