from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserSettings

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nationality = forms.CharField(max_length=100, required=False)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'nationality')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo', 'nationality', 
                 'city', 'mother_tongue', 'learning_language', 'religion', 
                 'caution_level']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'nationality': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'mother_tongue': forms.Select(attrs={'class': 'form-select'}),
            'learning_language': forms.Select(attrs={'class': 'form-select'}),
            'religion': forms.Select(attrs={'class': 'form-select'}),
            'caution_level': forms.Select(attrs={'class': 'form-select'}),
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['ai_enabled', 'tts_enabled', 'voice_choice', 'offline_mode', 'notifications_enabled']
        widgets = {
            'ai_enabled': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'tts_enabled': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'voice_choice': forms.Select(attrs={'class': 'form-select'}),
            'offline_mode': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }