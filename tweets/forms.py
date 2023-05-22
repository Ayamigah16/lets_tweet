from django import forms
from .models import Tweet

MAX_LENGTH = 280

# creating form for the tweet model
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet           # referencing the tweet model
        fields = ['content']     # using only the content feature

    # applying constraints to the content
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content
