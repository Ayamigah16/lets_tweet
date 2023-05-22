import random
from django.db import models

# Create your models here.
class Tweet(models.Model):
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    # TODO  -> More tweet features to add

    class Meta:
        ordering = ['-id']   # odering output with the latest tweet

    def serialize(self):
        return {
            "id" :self.id,
            "content" :self.content,
            "likes": random.randint(0, 500)
        }