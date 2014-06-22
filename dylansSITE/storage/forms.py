from django import forms
from models import Item


class ItemForm(forms.ModelForm):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'size': 60}), max_length=60)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 45}), max_length=200, required=False)
    
    