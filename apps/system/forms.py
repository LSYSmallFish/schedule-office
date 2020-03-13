from django import forms


class LoginForm(forms.Form):
    """用户登录表单"""
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
