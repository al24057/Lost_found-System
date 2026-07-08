# Lost_found_Web/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Lost_found_Web.models import Post, PostView

User = get_user_model()

# このファイル内のすべてのテストでデータベースへのアクセス（読み書き）を許可する
pytestmark = pytest.mark.django_db


class TestIndexView:
    """IndexView（name="home"）に関するテストクラス"""

    def test_get_requires_login(self, client):
        """1. 未ログインの場合：ログイン画面へリダイレクトされることを検証"""
        url = reverse('Lost_found_Web:home') 
        response = client.get(url)
        
        assert response.status_code == 302
        assert '/login/' in response.url


    def test_get_displays_open_posts_for_logged_in_user(self, client):
        """2. ログイン済みの場合：画面が正常に表示され、未解決の落とし物データがHTMLに含まれているかを検証"""
        
        # ── 準備 (Arrange) ──
        # テスト用のユーザーを作成し、クライアントをログイン状態にする
        user = User.objects.create_user(username="testuser", password="password123")
        client.login(username="testuser", password="password123")
        
        # 実際のPostモデルのフィールドに合わせてテストデータを2つ作成
        # （statusはデフォルトで 'open' になります）
        post1 = Post.objects.create(
            user=user,
            item="valuable",
            item_detail="黒いレザーの長財布（ロゴ入り）",
            color="black",
            location="classroom_building",
            floor="third"
        )
        post2 = Post.objects.create(
            user=user,
            item="electronic_device",
            item_detail="白いワイヤレスイヤホン（左耳のみ）",
            color="white",
            location="exchange_building",
            floor="first"
        )

        # ── 行動 (Act) ──
        # ホーム画面にGETリクエストを送る
        url = reverse('Lost_found_Web:home')
        response = client.get(url)

        # ── 検証 (Assert) ──
        # ステータスコードが200（成功）であることを確認
        assert response.status_code == 200
        
        # 正しいテンプレートが使われているか確認
        assert "Lost_found_Web/index.html" in [t.name for t in response.templates]
        
        # ビューからテンプレートに渡される context の中に、作成したデータが含まれているか確認
        assert post1 in response.context['posts']
        assert post2 in response.context['posts']
        
        # レンダリングされたHTMLの中に、画面に表示しているはずの文字が含まれているか確認
        html_content = response.content.decode('utf-8')
        
        # ⭕ 修正ポイント：item_detail の代わりに、実際にHTMLに出力している文字を検証する
        # post1 のデータ（valuable = 貴重品, classroom_building = 教室棟, third = 3階）
        assert "貴重品" in html_content
        assert "教室棟" in html_content
        assert "3階" in html_content
        
        # post2 のデータ（electronic_device = 電子機器..., exchange_building = 交流棟, first = 1階）
        assert "電子機器" in html_content
        assert "交流棟" in html_content
        assert "1階" in html_content
        
        
class TestDetailView:

    # -----------------------------------------------------------------
    # 1. GETリクエストのテスト（詳細表示 ＆ 履歴保存 ＆ 表示項目検証）
    # -----------------------------------------------------------------
    def test_get_detail_and_saves_history(self, client):
        """詳細画面にアクセスした際、画面が表示され、履歴が残り、指定の項目がHTMLに含まれるか検証"""
        # ── 準備 (Arrange) ──
        # 投稿者(owner)と、詳細を見る人(viewer)を作成
        owner = User.objects.create_user(username="owner_user", password="password")
        viewer = User.objects.create_user(username="viewer_user", password="password")
        client.login(username="viewer_user", password="password")
        
        # 表示対象の落とし物データを作成（実際のフィールド名に合わせる）
        post = Post.objects.create(
            user=owner,                   # 投稿者名用
            item="valuable",              # カテゴリ（貴重品）
            color="black",                # 色（黒）
            location="classroom_building", # 場所（教室棟）
            floor="third",                # 階数（3階 ※場所の詳細用）
            item_detail="このテキストは画面に表示されてはいけない" # アイテムの詳細
        )

        # ── 行動 (Act) ──
        url = reverse('Lost_found_Web:detail', kwargs={'pk': post.pk})
        response = client.get(url)

        # ── 検証 (Assert) ──
        assert response.status_code == 200
        assert "Lost_found_Web/detail.html" in [t.name for t in response.templates]
        
        # 1. 閲覧履歴が正しく保存されているかの検証
        assert PostView.objects.filter(user=viewer, post=post).count() == 1
        
        # 2. HTMLの表示内容の検証
        html_content = response.content.decode('utf-8')
        
        # ⭕ 表示されなければならない項目のチェック
        assert "owner_user" in html_content      # 投稿者名
        assert "貴重品" in html_content          # カテゴリ
        assert str(post.pk) in html_content      # 投稿ID
        assert "黒" in html_content              # 色（Choiceの日本語ラベル）
        assert "教室棟" in html_content          # 場所
        assert "3階" in html_content             # 場所の詳細（階数など）
        # ※ 投稿日や画像については、HTML側で {{ post.created_at }} や <img> タグが
        # 正しく記述されていれば、ステータス200の時点で描画が通っています。

        # ❌ 表示してはならない項目のチェック
        assert "このテキストは画面に表示されてはいけない" not in html_content # アイテムの詳細

    # -----------------------------------------------------------------
    # 2. POSTリクエストのテスト：正常な申請（未解決の場合）
    # -----------------------------------------------------------------
    def test_post_apply_success(self, client):
        """未解決の投稿に対して申請ボタンを押した際、申請が登録されリダイレクトされることを検証"""
        user = User.objects.create_user(username="applicant", password="password")
        owner = User.objects.create_user(username="owner")
        client.login(username="applicant", password="password")
        post = Post.objects.create(user=owner, item="valuable", status="open")

        url = reverse('Lost_found_Web:detail', kwargs={'pk': post.pk})
        response = client.post(url, data={'action': 'apply'})

        assert response.status_code == 302
        assert response.url == reverse('Lost_found_Web:home')
        assert user in post.applied_by.all()

    # -----------------------------------------------------------------
    # 3. POSTリクエストのテスト：不正な申請（解決済みの分岐ルート）
    # -----------------------------------------------------------------
    def test_post_apply_already_resolved(self, client):
        """既に解決済みの投稿に申請した場合、アラート画面が返ることを検証"""
        user = User.objects.create_user(username="applicant", password="password")
        owner = User.objects.create_user(username="owner")
        client.login(username="applicant", password="password")
        post = Post.objects.create(user=owner, item="valuable", status="resolved")

        url = reverse('Lost_found_Web:detail', kwargs={'pk': post.pk})
        response = client.post(url, data={'action': 'apply'})

        assert response.status_code == 200
        
        html_content = response.content.decode('utf-8')
        assert "既に解決済みのため、申請できません" in html_content
        assert user not in post.applied_by.all()
        
    # -----------------------------------------------------------------
    # 4. POSTリクエストのテスト：actionがapplyではない場合（★Partial解消用）
    # -----------------------------------------------------------------
    def test_post_action_not_apply(self, client):
        """【分岐網羅】actionがapply以外の場合、何も処理せずホームにリダイレクトされるか検証"""
        user = User.objects.create_user(username="test_user", password="password")
        client.login(username="test_user", password="password")
        post = Post.objects.create(user=user, item="valuable", status="open")

        url = reverse('Lost_found_Web:detail', kwargs={'pk': post.pk})
        
        # ⭕ action に 'apply' 以外のテキトーな文字（または空文字）を入れて送信する
        response = client.post(url, data={'action': 'invalid_action'})

        # 検証：if文の中身は通らず、そのままホームへリダイレクトされること
        assert response.status_code == 302
        assert response.url == reverse('Lost_found_Web:home')
        
    # -----------------------------------------------------------------
    # 5. GETリクエストのテスト：2回目以降の閲覧（★if not created の分岐網羅用）
    # -----------------------------------------------------------------
    def test_get_detail_updates_history_if_already_exists(self, client):
        """【分岐網羅】すでに閲覧履歴が存在する画面に再度アクセスした際、日時が更新されるか検証"""
        # 準備
        user = User.objects.create_user(username="repeat_viewer", password="password")
        client.login(username="repeat_viewer", password="password")
        post = Post.objects.create(user=user, item="valuable", status="open")

        url = reverse('Lost_found_Web:detail', kwargs={'pk': post.pk})
        
        # 1回目のアクセス（これで履歴データが新規作成され、created=True になる）
        response1 = client.get(url)
        assert response1.status_code == 200
        
        # 1回目の閲覧時刻を取得しておく
        first_history = PostView.objects.get(user=user, post=post)
        first_viewed_at = first_history.viewed_at

        # 2回目のアクセス（★これが if not created: の中身を通る！）
        response2 = client.get(url)
        assert response2.status_code == 200

        # 検証：データ件数は1件のままで増えていないこと（重複排除の確認）
        assert PostView.objects.filter(user=user, post=post).count() == 1
        
        # 検証：43〜44行目が実行され、閲覧日時（viewed_at）が新しく更新されていること
        second_history = PostView.objects.get(user=user, post=post)
        assert second_history.viewed_at > first_viewed_at