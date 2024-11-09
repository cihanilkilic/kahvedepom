# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='E-Posta', max_length=200, help_text='zorunlu')
    username = forms.CharField(label='Kullanıcı Adı', max_length=200, help_text='zorunlu')
    first_name = forms.CharField(label='Ad', max_length=30, help_text='adınızı girin')
    last_name = forms.CharField(label='Soyad', max_length=30, help_text='soyadınızı girin')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email


from .models import UserAddress

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['first_name', 'last_name', 'phone', 'city', 'district', 'mahalle', 'address_title', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }







from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Yeni Şifre",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Bootstrap class for styling
            #'placeholder': 'Yeni Şifre'  # Placeholder text
        })
    )
    new_password2 = forms.CharField(
        label="Yeni Şifre Tekrar",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
           # 'placeholder': 'Yeni Şifre Tekrar'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Yeni şifreler eşleşmiyor.")
        return cleaned_data