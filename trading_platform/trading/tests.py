# trading_platform/trading/tests.py
import sys
import os
import django
from dotenv import load_dotenv

# طباعة المسارات المستخدمة من قبل Python
print("Python Path:", sys.path)
print("Current Working Directory:", os.getcwd())

# إعداد Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trading_platform.config.settings")
django.setup()

# تحميل المتغيرات البيئية من .env
load_dotenv()

import openai
from django.conf import settings

# إعداد مفتاح API واختبار الاتصال بـ OpenAI
openai.api_key = settings.OPENAI_API_KEY
response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt="اختبر اتصال بسيط لتوليد استجابة.",
    max_tokens=50
)

print(response)
