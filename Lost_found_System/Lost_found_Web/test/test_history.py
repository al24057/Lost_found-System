import pytest
from django.contrib.auth.models import User
from Lost_found_Web.models import Post
from Lost_found_Web.services.history import Checkhistory

@pytest.mark.django_db
def test_history_services_all():
    # 1. 準備：テスト用ユーザーとデータを作成
    test_user = User.objects.create_user(username="testuser", password="password123")
    
    Post.objects.create(
        user=test_user,
        item="valuable",
        item_detail="黒い本革の財布",
        color="black",
        location="classroom_building",
        floor="first",
        status="open"
    )
    
    checker = Checkhistory()

    # 2. 実行パターン①：getpostid のテスト（これで半分の関数が動く）
    post_results = checker.getpostid(test_user.id)
    assert len(post_results) == 1

    # 3. 実行パターン②：getuserid のテスト（これで残りの関数も全部動く！）
    user_results = checker.getuserid(test_user.id)
    assert len(user_results) == 1