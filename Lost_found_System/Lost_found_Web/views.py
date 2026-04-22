from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, "Lost_found_Web/index.html")
    
    
index = IndexView.as_view()
