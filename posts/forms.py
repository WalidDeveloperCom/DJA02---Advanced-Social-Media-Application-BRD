from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class PostFilterForm(forms.Form):
    date_order = forms.ChoiceField(choices=[('latest', 'Latest'), ('oldest', 'Oldest')], required=False)
    media_type = forms.ChoiceField(choices=[('all', 'All'), ('text', 'Text Only'), ('image', 'With Image')], required=False)
    author = forms.CharField(required=False)
    search = forms.CharField(required=False)