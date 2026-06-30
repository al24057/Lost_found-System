from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import Post, PostView
# ==========================================
# C8 閲覧情報管理部
# ==========================================

# M5-8-1 投稿データ取得・検索モジュール
class PostSearcher:
    """閲覧に関する操作において，各メソッドで特定の条件を満たす投稿を取得するクラス"""
    
    @staticmethod
    def get_open_posts(text: str) -> list:
        """投稿の解決状況が未解決になっている投稿データを投稿日時が最新順に取得する．"""
        posts = Post.objects.filter(status='open').order_by(text)
        # エラー処理: 表示対象のデータが0件の場合は空リストをそのまま返却
        return list(posts)

    @staticmethod
    def get_post_by_id(pk: int) -> Post:
        """M5-3-2から入力された投稿IDに対応する投稿データを，データベースから取得する．"""
        # エラー処理: 投稿データが存在しない場合、404ページに遷移させる
        return get_object_or_404(Post, pk=pk)


# M5-8-2 申請データ登録モジュール
def register_application(user, post):
    """申請したユーザと投稿を受け取り，その投稿のapplied_byのデータベース項目に申請したユーザとして登録する．"""
    post.applied_by.add(user)
    return user


# M5-8-3 閲覧履歴データ保存モジュール
def browsing_history_save(user, post):
    """W4閲覧詳細画面を閲覧したユーザデータと，閲覧された投稿をM5-3-2から受け取り，閲覧履歴をデータベースに登録する．"""
    obj, created = PostView.objects.get_or_create(
        user=user,
        post=post
    )

    # エラー処理: 登録時にすでにそのユーザによる閲覧履歴があった場合は，閲覧日時を更新する
    if not created:
        obj.viewed_at = timezone.now()
        obj.save()
        
    return obj