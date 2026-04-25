from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse

ALLOWED_DOMAIN = "shibaura-it.ac.jp"

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
    
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email

        if not email:
            messages.error(request, "メールアドレスが取得できません")
            raise ImmediateHttpResponse(redirect("/login/"))

        if not email.endswith(f"@{ALLOWED_DOMAIN}"):
            messages.error(request, "学内メールアカウントでログインしてください")
            raise ImmediateHttpResponse(redirect("/login/"))