from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",  # Texte du label
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",  # Texte du label
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
