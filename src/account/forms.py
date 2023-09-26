from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Usuario

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Obligatorio. Ingrese un email valido')

    class Meta:
        model = Usuario
        fields = ("email", "username", "password1", "password2")

class AccountAuthenticationForm(forms.ModelForm):
    
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email o contraseña incorrectos")
            
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'profile_pic')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Usuario.objects.exclude(pk=self.instance.pk).get(email=email)
            except Usuario.DoesNotExist:
                return email
            raise forms.ValidationError('El email "%s" ya esta en uso.' % email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Usuario.objects.exclude(pk=self.instance.pk).get(username=username)
            except Usuario.DoesNotExist:
                return username
            raise forms.ValidationError('El nombre de usuario "%s" ya esta en uso.' % username)