from django import forms
from .models import Travel

class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['name', 'country', 'city', 'travel_type', 'start_date', 'residence', 'objectives']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Morocco Adventure 2025'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Morocco'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Marrakech'
            }),
            'travel_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'residence': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Hotel Riad Yasmine'
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Describe your travel objectives...'
            }),
        }