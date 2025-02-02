from django import forms
from django.core.exceptions import ValidationError

from .models import User
from .utils import is_string_alphanumeric, is_string_alphanumeric_white_space


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name']

    def clean_username(self) -> str:
        username = self.cleaned_data.get('username')
        if not is_string_alphanumeric(username):
            raise ValidationError('invalid username. only alphanumeric.')
        if User.is_username_exists(username=username):
            raise ValidationError('username already used. try other username.')
        return username
    
    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.is_email_exists(email=email):
            raise ValidationError('email already used. try other email.')
        return email
    
    def clean_name(self) -> str:
        name = self.cleaned_data.get('name')
        if not is_string_alphanumeric_white_space(name):
            raise ValidationError('invalid name. only alphanumeric.')
        return name
    
    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.generate_personal_ref_code()
        if commit:
            user.save()
        return user
    
class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=255, required=False)
    name = forms.CharField(max_length=255, required=False)
    password = forms.CharField(required=False)

    def clean_username(self) -> str | None:
        username = self.cleaned_data.get('username') if self.cleaned_data.get('username') else None
        if username and not is_string_alphanumeric(username):
            raise ValidationError('invalid username. only alphanumeric.')
        if username and User.is_username_exists(username=username):
            raise ValidationError('email already used. try other username.')
        return username
    
    def clean_email(self) -> str | None:
        email = self.cleaned_data.get('email') if self.cleaned_data.get('email') else None
        if email and User.is_email_exists(email=email):
            raise ValidationError('email already used. try other email.')
        return email
    
    def clean_name(self) -> str | None:
        name = self.cleaned_data.get('name') if self.cleaned_data.get('name') else None
        if name and not is_string_alphanumeric_white_space(name):
            raise ValidationError('invalid name. only alphanumeric.')
        return name
    
    def save(self, instance: User) -> User:
        for field in self.cleaned_data:
            if self.cleaned_data.get(field) and self.cleaned_data.get(field) is not None:
                if field == 'password':
                    instance.set_password(self.cleaned_data.get(field))
                else:
                    setattr(instance, field, self.cleaned_data.get(field))
        instance.save()
        return instance
    
class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True)

    @property
    def get_username(self) -> str:
        return self.cleaned_data.get('username')
    
    @property
    def get_password(self) -> str:
        return self.cleaned_data.get('password')
    

class InputReferralCode(forms.Form):
    referral_code = forms.CharField(min_length=10, max_length=10, required=True)

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')
        if not is_string_alphanumeric(referral_code):
            raise ValidationError('invalid referral code. only alphanumeric.')
        if not User.is_referral_code_exists(referral_code=referral_code):
            raise ValidationError('referral code not exists. try again')
        return referral_code
    
    def save(self, instance: User) -> User:
        referral_code = self.cleaned_data.get('referral_code')
        instance.set_referral_code(referral_code=referral_code)
        instance.save()
        return instance        