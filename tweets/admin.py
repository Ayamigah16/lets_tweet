from django.contrib import admin

from .models import Tweet, TweetLike
# Register your models here.

class TweetLikeAdmin(admin.TabularInline):     
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    class Meta:
        model = Tweet

    inlines = [TweetLikeAdmin]
    search_fields = ['content','user__username','user__email']
    list_display = ['__str__','user']

admin.site.register(Tweet, TweetAdmin)