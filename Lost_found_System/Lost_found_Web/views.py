from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/index.html")
    
class DetailView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/detail.html")
    
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
