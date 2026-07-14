"""
WSGI config for Lost_found_System project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lost_found_System.settings')

application = get_wsgi_application()

# Djangoの設定とアプリの読み込みを確実に完了させる
django.setup()

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        # メールアドレスは空文字 "" で作成します
        User.objects.create_superuser(username=username, email="", password=password)
        print(f"Superuser '{username}' created successfully.")
