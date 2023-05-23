from django.contrib import admin

from .models import Tweet
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    class Meta:
        model = Tweet

    search_fields = ['content','user__username','user__email']
    list_display = ['__str__','user']

admin.site.register(Tweet, TweetAdmin)