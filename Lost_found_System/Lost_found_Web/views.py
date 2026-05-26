from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone
from django.http import HttpResponse

class IndexView(LoginRequiredMixin, View):
    def get(self, request):       
        posts = Post.objects.filter(status='open').order_by('-created_at')
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
    
class PostPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Lost_found_Web/post.html")
    
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
