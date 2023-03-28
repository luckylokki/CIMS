from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUserModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = 'username', 'first_name', 'last_name', 'slack', 'email', 'password',
        widgets = {'password': forms.PasswordInput}
        help_texts = {'username': None}

    password1 = forms.CharField(max_length=32, label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUserModel.objects.get(username=username)
            raise ValidationError('User with this username is exists')
        except CustomUserModel.DoesNotExist:
            return username

    def clean(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            raise ValidationError('Passwords do not match')

    def create_user(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        slack = self.cleaned_data['slack']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        CustomUserModel.objects.create_user(username, email, password,first_name=first_name,last_name=last_name, slack=slack)


class SignInForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = 'username', 'password'
        widgets = {'password': forms.PasswordInput}
        help_texts = {'username': None}
        labels = {'username': 'Username', 'password': 'Password'}

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError("Invalid username or password, please try again")


class UserProfileEdit(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = 'first_name', 'last_name', 'email', 'slack'
        email = forms.EmailField
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def save(self, user: CustomUserModel):
        CustomUserModel.objects.filter(pk=user.pk).update(**self.cleaned_data)


class UserPasswordChange(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ('password',)
        widgets = {'password': forms.PasswordInput}
        labels = {'password': 'New Password'}

    password1 = forms.CharField(max_length=32, label='Confirm Password', widget=forms.PasswordInput)
    password_old = forms.CharField(max_length=32, label='Old Password', widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password != password1:
            raise ValidationError('Passwords do not match')

    def clean_password_old(self):
        password_old = self.cleaned_data['password_old']
        if not self.instance.check_password(password_old):
            raise ValidationError("Current password is not correct")

    def save(self, user: CustomUserModel):
        password = self.cleaned_data['password']
        password_hash = make_password(password, None, 'default')
        CustomUserModel.objects.filter(pk=user.pk).update(password=password_hash)
