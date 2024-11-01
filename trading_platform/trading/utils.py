# trading/utils.py
from openai import OpenAI
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import logging

# إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)

# إنشاء كائن OpenAI مع مفتاح API
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class TradingStrategyGenerator:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.error("OpenAI API key is missing in settings.")
            raise ValueError(_("OpenAI API key is missing or invalid."))

    def generate_strategy(self, profile):
        """توليد استراتيجية التداول بناءً على الملف الشخصي."""
        prompt = self._create_prompt(profile)
        logger.info("Generated Prompt for OpenAI: %s", prompt)

        try:
            # إرسال الطلب إلى OpenAI Chat API باستخدام الكائن client
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير في التداول والتحليل المالي."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000  # تأكد من وجود مساحة كافية للاستجابة
            )

            # تسجيل استجابة OpenAI API كاملة
            logger.info("Full OpenAI API Response: %s", response)

            # التحقق من وجود المحتوى المتوقع في الاستجابة
            if response and 'choices' in response and len(response.choices) > 0:
                strategy_content = response.choices[0].message.content
                return self._format_strategy(strategy_content)
            else:
                logger.error("No valid response from OpenAI API.")
                raise ValueError(_("لم يتم تلقي استجابة صالحة من OpenAI API."))

        except Exception as e:
            logger.error("Error generating strategy with OpenAI: %s", str(e))
            raise Exception(_("حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى."))

    def _create_prompt(self, profile):
        """إنشاء النص المبدئي استنادًا إلى بيانات المستخدم."""
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
        1. ملخص تنفيذي مختصر
        2. شروط الدخول
        3. شروط الخروج
        4. إدارة المخاطر
        5. إدارة رأس المال
        6. المؤشرات المستخدمة
        7. الجدول الزمني
        8. نصائح وتوصيات

        يجب أن تكون الاستراتيجية موجزة بحدود 100 إلى 150 كلمة، ومركزة على تقديم خطوات عملية قابلة للتنفيذ.
        """
        return prompt

    def _format_strategy(self, content):
        """تنسيق محتوى الاستراتيجية."""
        return content

    def _create_prompt(self, profile):
        """إنشاء نص المبدئي استنادًا إلى بيانات المستخدم."""
        prompt = f"""
        قم بإنشاء استراتيجية تداول واضحة، مفصلة، ولكن مختصرة بناءً على المعلومات التالية:

        مستوى الخبرة: {profile.get_experience_level_display()}
        أسلوب التداول: {profile.get_trading_style_display()}
        إدارة المخاطر: {profile.risk_management}
        الأصول المفضلة: {profile.favorite_assets}
        الأهداف المالية: {profile.financial_goals}
        ساعات التداول: {profile.trading_hours}
        نوع التحليل: {profile.get_analysis_type_display()}

        يجب أن تتضمن الاستراتيجية:
        1. ملخص تنفيذي مختصر
        2. شروط الدخول
        3. شروط الخروج
        4. إدارة المخاطر
        5. إدارة رأس المال
        6. المؤشرات المستخدمة
        7. الجدول الزمني
        8. نصائح وتوصيات

        يجب أن تكون الاستراتيجية موجزة بحدود 100 إلى 150 كلمة، ومركزة على تقديم خطوات عملية قابلة للتنفيذ.
        """
        return prompt

    def _format_strategy(self, content):
        """تنسيق محتوى الاستراتيجية."""
        return content
