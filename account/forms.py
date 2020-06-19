from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.conf import settings
from django.conf.urls.static import static
from . import models

class SignupUserForm(UserCreationForm):
    full_name = forms.CharField()

    class Meta:
        model = User
        fields = ('full_name','username','email','password1','password2')


class UpdateProfileForm(forms.ModelForm):
    full_name = forms.CharField()
    bio = forms.CharField(widget=forms.TextInput({}), required=False)
    picture = forms.FileField(required=False)

    class Meta:
        model = models.Profile
        fields = ['full_name','bio','picture']

    def save(self, commit=True):
        profile = super().save(commit=False)   
        profile.full_name = self.cleaned_data.get('full_name')
        profile.bio = self.cleaned_data.get('bio')
        profile.picture = self.cleaned_data.get('picture')

        if commit:
            profile.save()
        return profile

class LoginForm(forms.Form):
    username = forms.CharField();
    password = forms.CharField();
    
    class Meta:
        model = User
        fields = ['username','password']
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("This username does not exist. \
                                            Please enter a valid username."
                                        )
        return username


class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email',]

        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }





