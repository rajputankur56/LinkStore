from django import forms
from .models import Link

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ('link', 'title', 'category', 'description', 'favorite')
