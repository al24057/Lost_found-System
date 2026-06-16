from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .forms import PostForm

# 💡 変更：新しく作成したサービス関数のみをインポート（tempfileやos, detect_lost_item はビューから削除）
from .services.image_analy import analyze_uploaded_image

class IndexView(LoginRequiredMixin, View):
    def get(self, request):       
        posts = Post.objects.filter(status='open').order_by('-created_at') #この場所の関数を作らなければいけない(返り値が必要)
        return render(request, "Lost_found_Web/index.html", {'posts':posts})
    
class DetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        obj, created = PostView.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            obj.viewed_at = timezone.now()
            obj.save()
        
        return render(request, "Lost_found_Web/detail.html", {'post': post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        action = request.POST.get('action')

        if action == 'apply':
            if post.status == 'resolved':
                return HttpResponse('''
                    <script>
                        alert("この投稿は既に解決済みのため、申請できません。");
                        window.location.href = "/";
                    </script>
                ''')
            post.applied_by.add(request.user)
        
        return redirect('Lost_found_Web:home')
    
class PostPageView(LoginRequiredMixin, View):#投稿ページ
    def get(self, request, pk=None):
        if pk:
            post_instance = get_object_or_404(Post, pk=pk, user=request.user)
            form = PostForm(instance=post_instance)
        else:
            form = PostForm()
        return render(request, "Lost_found_Web/post.html", {'form': form})

    def post(self, request, pk=None):
        if 'analyze' in request.path:
            if request.FILES.get('image'):
                image_file = request.FILES['image']
                result_data = analyze_uploaded_image(image_file)
                
                if result_data.get('status') == 'error':
                    status_code = result_data.pop('status_code', 400)
                    return JsonResponse(result_data, status=status_code)
                    
                return JsonResponse(result_data)
            return JsonResponse({'status': 'error', 'message': '画像が正しく送信されませんでした。'}, status=400)
        
        if pk:
            post_instance = get_object_or_404(Post, pk=pk, user=request.user)
            form = PostForm(request.POST, request.FILES, instance=post_instance)
        else:
            form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_instance = form.save(commit=False)
            if not pk:
                post_instance.user = request.user
            post_instance.save()
            return redirect('Lost_found_Web:home')
        return render(request, "Lost_found_Web/post.html", {'form': form})

    # ==========================================================
    # 💡 修正：独立した関数にせず、既存のクラス内メソッドとして定義
    # ==========================================================
    def analyze_image(self, request):
        if request.method == 'POST' and request.FILES.get('image'):
            image_file = request.FILES['image']
            
            # サービス層の関数を呼び出して処理を実行
            result_data = analyze_uploaded_image(image_file)
            
            # サービス側でエラーハンドリングされた場合の処理
            if result_data.get('status') == 'error':
                status_code = result_data.pop('status_code', 400)
                return JsonResponse(result_data, status=status_code)
                
            return JsonResponse(result_data)
            
        return JsonResponse({'status': 'error', 'message': '画像が正しく送信されませんでした。'}, status=400)
    
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/search.html")
    
class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/history.html")
    
index = IndexView.as_view()
detail = DetailView.as_view()
post = PostPageView.as_view()
search = SearchView.as_view()
history = HistoryView.as_view()

# 💡 修正：クラスの外に関数を作らず、既存クラスのメソッドを views.analyze として割り当て
analyze = PostPageView().analyze_image