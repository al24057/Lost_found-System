from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
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
        
        return render(request, "Lost_found_Web/detail.html")
    
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
