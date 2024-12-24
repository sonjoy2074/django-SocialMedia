from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=264, blank=True, null=True)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upload_date',]
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} liked {}'.format(self.user.username, self.post.caption)  