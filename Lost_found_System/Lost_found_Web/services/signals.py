from allauth.socialaccount.signals import pre_social_login, social_account_added
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from .user_composition import RegisterUser, DeleteUser

# ② ユーザ名生成（保存後に安全に実行）
@receiver(user_signed_up)
def set_username(sender, request, user, **kwargs):
    email = user.email
    student_id = email.split("@")[0]
    base_name = user.first_name or "user"

    username = f"{base_name}_{student_id}"

    # 重複回避
    original = username
    i = 1
    from django.contrib.auth import get_user_model
    User = get_user_model()

    while User.objects.filter(username=username).exists():
        username = f"{original}_{i}"
        i += 1

    user.username = username
    RegisterUser(user)


# ✔ 通常登録を禁止（超重要）
@receiver(user_signed_up)
def block_non_google_signup(request, user, **kwargs):
    # socialaccountが無い = 通常登録
    if not user.socialaccount_set.exists():
        DeleteUser(user)
        raise PermissionDenied("Googleログインのみ許可されています")