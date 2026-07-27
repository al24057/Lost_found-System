from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='lost_items/', null=False, blank=False)
    ITEM_CHOICES = [
        ('umbrella', '傘'),
        ('stationary', '文房具'),
        ('electronic_device', '電子機器および周辺機器(スマホ、イヤホンなど)'),
        ('valuable', '貴重品(財布、鍵など)'),
        ('book', '本(教科書、ノートなど)'),
        ('daily', '日用品(水筒、眼鏡など)'),
        ('other', 'その他'),
    ]
    
    COLOR_CHOICES = [
        ('red', '赤'),
        ('blue', '青'),
        ('black', '黒'),
        ('white', '白'),
        ('gray', '灰'),
        ('brown', '茶'),
        ('orange', '橙'),
        ('yellow', '黄'),
        ('yellow_green', '黄緑'),
        ('green', '緑'),
        ('light_blue', '水色'),
        ('purple', '紫'),
    ]
    
    LOCATION_CHOICE = [
        ('outdoor', '屋外'),
        ('classroom_building', '教室棟'),
        ('headquarters_building', '本部棟'),
        ('exchange_building', '交流棟'),
        ('research_building', '研究棟'),
        ('community_space', '有元史郎記念校友会館交流プラザ'),
        ('other', 'その他'),
    ]
    
    FLOOR_CHOICES = [
        ('basement', '地下1階'),
        ('first', '1階'),
        ('second', '2階'),
        ('third', '3階'),
        ('fourth', '4階'),
        ('fifth', '5階'),
        ('sixth', '6階'),
        ('seventh', '7階'),
        ('eighth', '8階'),
        ('ninth', '9階'),
        ('tenth', '10階'),
        ('eleventh', '11階'),
        ('twelveth', '12階'),
        ('thirteenth', '13階'),
        ('fourteenth', '14階'),
    ]
    
    item = models.CharField(max_length=30, choices=ITEM_CHOICES, blank=False, null=False)
    item_detail = models.CharField(max_length=100, blank=True)
    
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=False, null=False)
    
    location = models.CharField(max_length=50, choices=LOCATION_CHOICE, blank=False, null=False)
    floor = models.CharField(max_length=15, choices=FLOOR_CHOICES, blank=False, null=False)
    
    location_detail = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(choices=[('open', '未解決'), ('resolved', '解決済')], default='open')
    applied_by = models.ManyToManyField(User, blank=True, related_name="applied_posts", verbose_name="申請したユーザー一覧")
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="posts_resolved")
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        floor = self.get_floor_display() if self.floor else ""
        return f"{self.get_item_display()} / {self.get_color_display()} / {self.get_location_display()} {floor}"
    
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        local_time = timezone.localtime(self.viewed_at)
        return f"{self.user.username} が {self.post} を {local_time.strftime('%Y-%m-%d %H:%M')} に閲覧"
    
@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    """
    レコードが削除されたら、紐付いている画像ファイルも物理的に削除する
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
