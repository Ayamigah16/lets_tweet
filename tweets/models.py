import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


# Create your models here.
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='tweet_user', blank=True,through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO  -> More tweet features to add

    class Meta:
        ordering = ['-id']   # odering output with the latest tweet

    def __str__(self):
        return self.content

    def serialize(self):
        return {
            "id" :self.id,
            "content" :self.content,
            "likes": random.randint(0, 500)
        }