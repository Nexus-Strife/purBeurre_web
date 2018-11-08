from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm


def index(request):
    return render(request, "web_app/index.html")


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            return redirect('../login/')

        else:
            pass

    else:
        form = RegisterForm()

    return render(request, "web_app/register.html", locals())


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('/')
            else:
                return redirect('../register/')
        else:
            pass
    else:
        form = LoginForm()

    return render(request, "web_app/connexion.html", locals())


def test(request):
    return HttpResponseRedirect(reverse(''))
