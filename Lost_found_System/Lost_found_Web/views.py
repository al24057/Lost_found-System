from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, PostView
from django.utils import timezone
from datetime import timedelta

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        expired_date = timezone.now() - timedelta(days=14)
        Post.objects.filter(status='resolved', resolved_at__lte=expired_date).delete()
        status_filter = request.GET.get('status', 'open')
        if status_filter == 'resolved':
            sort_order = '-resolved_at'
        else:
            sort_order = '-created_at'
        posts = Post.objects.filter(status=status_filter).order_by(sort_order)
        return render(request, "Lost_found_Web/index.html", {'posts':posts, 'current_status': status_filter})
    
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

        if action == 'resolve':
            post.status = 'resolved'
            post.resolved_by = request.user
            post.resolved_at = timezone.now()
            post.save()
        
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
