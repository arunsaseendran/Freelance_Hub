from django import forms
from .models import Service, Category, SubCategory

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'subcategory', 'title', 'description', 'price', 'duration', 'image', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories to freelancers
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by('name')
        
        for field in self.fields:
            if field == 'is_active':
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            elif field == 'description':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'rows': 4})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class ServiceSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search services...'
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    area = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Area'
    }))
    pincode = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pincode'
    }))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Min Price'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Max Price'
    }))
