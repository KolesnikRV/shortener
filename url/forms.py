from django import forms

from .models import Url


class UrlForm(forms.ModelForm):
    '''Form for Url model'''
    class Meta:
        model = Url
        fields = ('full_url', 'short_url')
