from django import forms
from django.core.exceptions import ValidationError

from .models import User


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name']

    def clean_username(self) -> str:
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('username already used. try other username.')
        return username
    
    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('email already used. try other email.')
        return email
    
    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.generate_personal_ref_code()
        if commit:
            user.save()
        return user
    
class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)

    @property
    def get_username(self) -> str:
        return self.cleaned_data.get('username')
    
    @property
    def get_password(self) -> str:
        return self.cleaned_data.get('password')