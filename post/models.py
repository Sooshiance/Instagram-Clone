from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    txt        = models.CharField(max_length=8000)
    media_file = models.FileField(upload_to='post/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    txt  = models.CharField(max_length=8000)
    
    def __str__(self) -> str:
        return f"{self.post} {self.user}"
