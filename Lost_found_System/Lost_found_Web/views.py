from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone
from django.http import HttpResponse
from .services.search import search as search_logic
from .services.detail import PostSearcher, register_application, browsing_history_save

class IndexView(LoginRequiredMixin, View):
    def get(self, request):       
       # text='-created_at' を定義して get_open_posts に渡す
        text = '-created_at'      
        posts = PostSearcher.get_open_posts(text=text)
        return render(request, "Lost_found_Web/index.html", {'posts': posts})
    
    
class DetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = PostSearcher.get_post_by_id(pk=pk)
        
       # user=request.user を定義して M5-8-3 に引き渡す
        user = request.user
        browsing_history_save(user=user, post=post)
        
        return render(request, "Lost_found_Web/detail.html", {'post': post})
    
    def post(self, request, pk):
       # M5-8-1 (get_post_by_idメソッド) で投稿を取得
        post = PostSearcher.get_post_by_id(pk=pk)
        action = request.POST.get('action')

        if action == 'apply':
            if post.status == 'resolved':
                return HttpResponse('''
                    <script>
                        alert("この投稿は既に解決済みのため、申請できません。");
                        window.location.href = "/";
                    </script>
                ''')
            
            # user=request.user を定義して M5-8-2 に引き渡す
            user = request.user
            register_application(user=user, post=post)
        
        return redirect('Lost_found_Web:home')
    
class PostPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/post.html")
    
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        # 1. 画面（URLのクエリパラメータ）から検索条件をゲットする
        item = request.GET.get('item', 'all')
        color = request.GET.get('color', 'all')
        location = request.GET.get('location', 'all')
        floor = request.GET.get('floor', 'all')

        # 2. ボタンが押された（検索が実行された）かどうかを判定
        # 何かしら条件が指定されている、またはクエリパラメータが存在する場合
        is_searched = any(k in request.GET for k in ['item', 'color', 'location', 'floor'])

        posts = []
        if is_searched:
            # 3. せっかくインポートしてある search.py のロジックをここで呼び出す！
            posts = search_logic(item=item, color=color, location=location, floor=floor)

        # 4. テンプレート（search.html）に結果と、選んだ条件をセットして返す
        context = {
            'posts': posts,
            'is_searched': is_searched,
            'query_params': {
                'item': item,
                'color': color,
                'location': location,
                'floor': floor,
            }
        }
        return render(request, "Lost_found_Web/search.html", context)
    
class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/history.html")
    
    
index = IndexView.as_view()
detail = DetailView.as_view()
post = PostPageView.as_view()
search = SearchView.as_view()
history = HistoryView.as_view()
