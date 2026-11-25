
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Product


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email








class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        #fields = ['name','price','description','image']
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter product name'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter product price'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter product details'}),
            'image': forms.FileInput(attrs={'class':'form-control','placeholder':'Upload file','accept':".pdf, image/png, image/jpeg"})
        }
    
    