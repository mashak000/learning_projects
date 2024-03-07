from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField



class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name='usersfollowers', symmetrical=False)
    followings = models.ManyToManyField('self', blank=True, related_name='usersfollowings', symmetrical=False)
    image = models.URLField(max_length=200, blank=True)
    color = ColorField(default='#FF0000')

class Post(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1, related_name="network_user_related")
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.text}"

class Like(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1, related_name="likedby")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, default=0, related_name="postlikes")

    def __str__(self):
        return f"{self.post} liked by {self.who}"