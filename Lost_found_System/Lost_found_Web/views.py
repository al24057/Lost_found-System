from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post

class IndexView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        return render(request, "Lost_found_Web/index.html", {'posts':posts})
    
class DetailView(View):
    def get(self, request,pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, "Lost_found_Web/detail.html",{'post':post})
    
class PostView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/post.html")
    
class SearchView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/search.html")
    
class HistoryView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/history.html")
    
    
index = IndexView.as_view()
detail = DetailView.as_view()
post = PostView.as_view()
search = SearchView.as_view()
history = HistoryView.as_view()
