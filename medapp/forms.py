from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
            
    def __init__(self,*args,**kvargs):
        super(CommentForm,self).__init__(*args,**kvargs)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'search-field',
        'placeholder': 'Axtar'
    }))


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ('tag',)
            
    def __init__(self,*args,**kvargs):
        super(BlogForm,self).__init__(*args,**kvargs)
