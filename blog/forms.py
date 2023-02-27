from django import forms
from .models import Condo, ReviewRating

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_title', 'review', 'customer_service', 'build_quality', 'amenities', 'location', 'would_reviewer_recommend']
        # fields = ('__all__')