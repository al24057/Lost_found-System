# ==============================================================================
# ファイル名: search.py
# 機能概要: 設計書の「C5 検索処理部」および「C9 検索情報管理部」の全機能を実装。
#           ユーザーが指定した条件でデータベースから未解決の落とし物を絞り込みます。
# ==============================================================================

from ..models import Post

def search(item=None, color=None, location=None, floor=None):
    """
    指定された条件（カテゴリー、カラー、拾得場所、階層）で未解決の落とし物を検索する。
    すべての引数が None、または 'all' の場合は、すべての未解決データを返す。
    """
    # 1. まずはすべての投稿（落とし物データ）をベースにする
    queryset = Post.objects.all()

    # 2. カテゴリーで絞り込み（値が存在し、かつ 'all' 以外の場合のみ適用）
    if item and item != 'all':
        queryset = queryset.filter(item=item)

    # 3. カラーで絞り込み
    if color and color != 'all':
        queryset = queryset.filter(color=color)

    # 4. 拾得場所で絞り込み
    if location and location != 'all':
        queryset = queryset.filter(location=location)

    # 5. 階層で絞り込み
    if floor and floor != 'all':
        queryset = queryset.filter(floor=floor)

    # 6. 条件にマッチしたデータを、投稿日時の新しい順（降順）にして返す
    return queryset.order_by('-created_at')