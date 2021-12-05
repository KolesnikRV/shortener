from django import forms

from .models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ('full_url', 'short_url')
