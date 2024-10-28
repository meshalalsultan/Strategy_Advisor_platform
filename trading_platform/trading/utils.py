import openai
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class TradingStrategyGenerator:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def generate_strategy(self, profile):
        """Generate a trading strategy based on user profile."""
        prompt = self._create_prompt(profile)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """أنت خبير في التداول والتحليل المالي. 
                    مهمتك إنشاء استراتيجيات تداول مخصصة بناءً على بيانات المتداول."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            strategy_content = response.choices[0].message.content
            return self._format_strategy(strategy_content)
            
        except Exception as e:
            raise Exception(_("حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى."))

    def _create_prompt(self, profile):
        """Create a prompt for ChatGPT based on user profile."""
        prompt = f"""
        قم بإنشاء استراتيجية تداول مفصلة بناءً على المعلومات التالية:

        مستوى الخبرة: {profile.get_experience_level_display()}
        أسلوب التداول: {profile.get_trading_style_display()}
        إدارة المخاطر: {profile.risk_management}
        الأصول المفضلة: {profile.favorite_assets}
        الأهداف المالية: {profile.financial_goals}
        ساعات التداول: {profile.trading_hours}
        نوع التحليل: {profile.get_analysis_type_display()}

        يجب أن تتضمن الاستراتيجية:
        1. ملخص تنفيذي
        2. شروط الدخول
        3. شروط الخروج
        4. إدارة المخاطر
        5. إدارة رأس المال
        6. المؤشرات المستخدمة
        7. الجدول الزمني
        8. نصائح وتوصيات

        قم بتنسيق الاستراتيجية بشكل منظم ومقروء.
        """
        return prompt

    def _format_strategy(self, content):
        """Format the strategy content."""
        # Add any additional formatting if needed
        return content