from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
#ユーザー情報処理部

def RegisterUser(user):
    user.save()



def DeleteUser(user):
    user.delete()
