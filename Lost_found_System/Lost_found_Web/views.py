from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .forms import PostForm
from .services.analy import detect_lost_item
import tempfile
import os

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
            post.applied_by.add(request.user)  #データベースを示している
        
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
    
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/search.html")
    
class HistoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/history.html")
    
# ==========================================================
# 💡 画像解析・連携用ビュー関数
# ==========================================================
def analyze_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # 1. 渡された画像ファイルを一時ファイルとしてサーバーに保存し、パスを生成
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # 2. analy.py の関数に一時ファイルのパスを渡して解析を実行
            # 返り値は (label, color_tag) のタプルを想定
            analysis_result = detect_lost_item(temp_file_path)
            
            if not analysis_result:
                return JsonResponse({'status': 'error', 'message': '物体を検出できませんでした。'}, status=200)
                
            detected_label, detected_color = analysis_result
            
            # 3. 💡 マッピング処理：検出された文字を models.py の Choice キーに変換
            # --- 色の変換テーブル ---
            COLOR_MAP = {
                '赤': 'red', '青': 'blue', '黒': 'black', '白': 'white',
                '灰': 'gray', '茶': 'brown', '橙': 'orange', '黄': 'yellow',
                '黄緑': 'yellow_green', '緑': 'green', '水': 'light_blue', '紫': 'purple'
            }
            
            # --- アイテム名の変換テーブル ---
            # ※ YOLOモデルが返すラベル名（英語か日本語か）に合わせて右側（models.pyのキー）に変換します
            ITEM_MAP = {
                '傘': 'umbrella', 'umbrella': 'umbrella',
                'ペン': 'stationary', '消しゴム': 'stationary', 'pen': 'stationary', 'eraser': 'stationary',
                'スマホ': 'electronic_device', 'phone': 'electronic_device',
                '財布': 'valuable', 'wallet': 'valuable',
                '本': 'book', 'book': 'book',
                '水筒': 'daily',
            }
            
            # 辞書から該当するキーを取得（見つからない場合は 'other' やデフォルトなしにする）
            mapped_color = COLOR_MAP.get(detected_color, 'black') # デフォルト黒
            mapped_item = ITEM_MAP.get(detected_label, 'other')    # デフォルトその他
            
            result_data = {
                'status': 'success',
                'item': mapped_item,
                'color': mapped_color,
            }
            return JsonResponse(result_data)
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'解析中にエラーが発生しました: {str(e)}'}, status=500)
            
        finally:
            # 4. 用が済んだ一時ファイルを物理削除
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        
    return JsonResponse({'status': 'error', 'message': '画像が正しく送信されませんでした。'}, status=400)
    
index = IndexView.as_view()
detail = DetailView.as_view()
post = PostPageView.as_view()
search = SearchView.as_view()
history = HistoryView.as_view()
analyze = analyze_image
