from django import forms
from .models import Condo

class CondoForm(forms.ModelForm):
    class Meta:
        model = Condo
        fields = ('__all__')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Condo'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Condo
        fields = ('__all__')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Condo'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }