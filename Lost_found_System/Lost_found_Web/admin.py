from django.contrib import admin
from.models import Post, PostView

class PostAdmin(admin.ModelAdmin):
    # 一覧画面で見たい項目（ID、アイテム名、投稿者、状態など）
    list_display = ('id', 'item', 'user', 'created_at', 'status')
    
    # ★ IDやアイテム詳細、投稿者名で検索できるようにする
    search_fields = ('id', 'item_detail', 'user__username')
    
    # 右側にフィルター（絞り込み）機能をつけるとさらに便利です
    list_filter = ('status', 'item', 'created_at')

# カスタマイズしたPostAdminと一緒に登録
admin.site.register(Post, PostAdmin)

# PostViewは今のままでもOK
admin.site.register(PostView)
