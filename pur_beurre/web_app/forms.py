from django import forms


class LoginForm(forms.Form):

    nickname = forms.CharField(label="Votre pseudo", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Votre pseudo', 'class': 'form-control'}))
    password = forms.CharField(label="Votre mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}))


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'form-control'}))
    last_name = forms.CharField(label="Nom de famille", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nom de famille', 'class': 'form-control'}))
    nickname = forms.CharField(label="Pseudo", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Pseudo', 'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}))
