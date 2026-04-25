from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    # ✔ サインアップ強制許可（超重要）
    def is_open_for_signup(self, request, sociallogin):
        return True

    # ✔ signup画面をスキップしてホームへ
    def get_signup_redirect_url(self, request):
        return "/"

    # ✔ ログイン後もホームへ
    def get_login_redirect_url(self, request):
        return "/"