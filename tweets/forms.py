from django.conf import settings
from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
# creating form for the tweet model
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet           # referencing the tweet model
        fields = ['content']     # using only the content feature

    # applying constraints to the content
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content
