import openai
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import logging



# إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)

class TradingStrategyGenerator:
    def __init__(self):
        # تأكيد تحميل مفتاح API
        openai.api_key = settings.OPENAI_API_KEY
        if not openai.api_key:
            logger.error("OpenAI API key is missing in settings.")
            raise ValueError(_("OpenAI API key is missing or invalid."))

    def generate_strategy(self, profile):
        prompt = self._create_prompt(profile)
        logger.info("Generated Prompt for OpenAI: %s", prompt)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير في التداول والتحليل المالي."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            logger.info("OpenAI Response: %s", response)

            if 'choices' in response and len(response.choices) > 0:
                strategy_content = response.choices[0].message.content
                return self._format_strategy(strategy_content)
            else:
                logger.error("No valid response from OpenAI API.")
                raise ValueError(_("لم يتم تلقي استجابة صالحة من OpenAI API."))

        except Exception as e:
            logger.error("Error in OpenAI API call: %s", str(e))
            raise Exception(_("حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى."))

    def _create_prompt(self, profile):
        return f"""
        قم بإنشاء استراتيجية تداول بناءً على:
        مستوى الخبرة: {profile.get_experience_level_display()}
        أسلوب التداول: {profile.get_trading_style_display()}
        إدارة المخاطر: {profile.risk_management}
        الأصول المفضلة: {profile.favorite_assets}
        الأهداف المالية: {profile.financial_goals}
        ساعات التداول: {profile.trading_hours}
        نوع التحليل: {profile.get_analysis_type_display()}
        """

    def _format_strategy(self, content):
        return content
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def generate_strategy(self, profile):
        prompt = self._create_prompt(profile)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير في التداول والتحليل المالي."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(_("حدث خطأ أثناء إنشاء الاستراتيجية. يرجى المحاولة مرة أخرى."))

    def _create_prompt(self, profile):
        return f"""
        قم بإنشاء استراتيجية تداول بناءً على:
        مستوى الخبرة: {profile.get_experience_level_display()}
        أسلوب التداول: {profile.get_trading_style_display()}
        إدارة المخاطر: {profile.risk_management}
        الأصول المفضلة: {profile.favorite_assets}
        الأهداف المالية: {profile.financial_goals}
        ساعات التداول: {profile.trading_hours}
        نوع التحليل: {profile.get_analysis_type_display()}
        """
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def generate_strategy(self, profile):
        """Generate a trading strategy based on user profile."""
        prompt = self._create_prompt(profile)
        logger.info("Generated Prompt: %s", prompt)

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
            
            # تسجيل استجابة OpenAI API بالكامل
            logger.info("OpenAI Response: %s", response)

            # تحقق من وجود المحتوى المتوقع في الاستجابة
            if 'choices' in response and len(response.choices) > 0:
                strategy_content = response.choices[0].message.content
                return self._format_strategy(strategy_content)
            else:
                logger.error("No valid response from OpenAI API.")
                raise Exception(_("لم يتم تلقي استجابة صالحة من OpenAI API."))

        except Exception as e:
            logger.error("Error generating strategy with OpenAI: %s", str(e))
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
