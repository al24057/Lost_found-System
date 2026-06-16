from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'item', 'item_detail', 'color', 'location', 'floor', 'location_detail']