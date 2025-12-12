from django import forms
from .models import Review, ReviewResponse

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                                  attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                            'placeholder': 'Share your experience...'}),
        }


class ReviewResponseForm(forms.ModelForm):
    class Meta:
        model = ReviewResponse
        fields = ['response_text']
        widgets = {
            'response_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                   'placeholder': 'Your response...'}),
        }
