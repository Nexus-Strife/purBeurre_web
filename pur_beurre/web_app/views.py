from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from django.contrib.auth import logout as out
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, SearchForm, SaveForm
from .models import Products
import psycopg2

hostname = 'localhost'
user = 'postgres'
password = 'C1li2tn45!'
database = 'pur_beurre'


def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('results/' + product + '/')
        else:
            form = SearchForm()

    else:
        form = SearchForm()
        return render(request, "web_app/index.html", locals())


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
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
                log(request, user)
                return redirect('../index/')
            else:
                return redirect('../register/')
        else:
            pass
    else:
        form = LoginForm()

    return render(request, "web_app/connexion.html", locals())


def logout(request):
    out(request)
    return redirect('../login/')


@login_required
def my_account(request):

    return render(request, "web_app/account.html", locals())


def results(request, product):
    form = SaveForm()
    conn = None
    conn = psycopg2.connect(host=hostname, user=user, password=password, database=database)
    cur = conn.cursor()
    prods = Products.objects.filter(name__contains=product).order_by('grade')

    try:
        searched = get_object_or_404(Products, name__contains=product)

        if searched is None:
            try:
                searched = get_object_or_404(Products, name__contains=product)
            except MultipleObjectsReturned:
                searched = Products.objects.filter(name__contains=product).first()
        else:
            pass

    except MultipleObjectsReturned:
        searched = Products.objects.filter(name__iexact=product).first()

    return render(request, "web_app/results.html", locals())


def details(request, product):
    detailed_prod = Products.objects.filter(name__iexact=product).first()
    return render(request, "web_app/details.html", locals())


def test(request):
    form = SaveForm()
    return render(request, "web_app/page_test.html", locals())
