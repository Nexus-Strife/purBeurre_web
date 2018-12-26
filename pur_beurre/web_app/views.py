from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
from django.contrib.auth import logout as out
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from .forms import LoginForm, RegisterForm, SearchForm, SaveForm, SearchForm_NavBar
from .models import Products, Favs
import psycopg2

hostname = 'localhost'
user = 'postgres'
password = 'C1li2tn45!'
database = 'pur_beurre'


def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('results/' + product + '/')
        else:
            form = SearchForm()
            form_nav = SearchForm_NavBar()

    else:
        form = SearchForm()
        form_nav = SearchForm_NavBar()
        return render(request, "web_app/index.html", locals())


def legals(request):

    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()

    return render(request, "web_app/legals.html", locals())


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

    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()

    return render(request, "web_app/account.html", locals())


def results(request, product):

    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()

    prods = Products.objects.raw("SELECT * FROM web_app_products WHERE name LIKE %(p)s ORDER by grade ASC", {"p": "%{}%".format(product.replace(' ', '%'))})

    try:
        searched = get_object_or_404(Products, name__icontains=product)

    except MultipleObjectsReturned:
        searched = Products.objects.filter(name__icontains=product).first()

    return render(request, "web_app/results.html", locals())


def details(request, product):

    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()

    detailed_prod = Products.objects.filter(name__iexact=product).first()
    return render(request, "web_app/details.html", locals())


def saveproduct(request):
    search = request.GET.get('searched')
    searched = Products.objects.filter(name__iexact=search)
    current_user = request.user
    id = request.GET.get('value')

    if search == "":
        try:
            fav = Favs(prod_id=id, prod_substitute_id=id, user_id=current_user.id)
            fav.save()
        except IntegrityError:
            print('Une erreur sauvage apparait !')
        data = {'respond': id}
        return JsonResponse(data)

    else:
        try:
            for elm in searched:
                id_prod = elm.id
            fav = Favs(prod_id=id_prod, prod_substitute_id=id, user_id=current_user.id)
            fav.save()
        except IntegrityError:
            print('Erreur...erreur')
        data = {'respond': id}
        return JsonResponse(data)


def my_favs(request):

    current_user = request.user
    curr_id = current_user.id
    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()

    favs_prod = Products.objects.raw("SELECT waf.prod_id as prod_id, wap.name as name, waf.id, wap.img_url as image"
                                " from web_app_favs waf"
                                " INNER JOIN web_app_products wap ON waf.prod_id = wap.id WHERE user_id = %s", (curr_id, ))

    favs_sub = Products.objects.raw("SELECT waf.prod_substitute_id as sub_prod_id, wap.name as name, waf.id, wap.img_url as img"
                                " from web_app_favs waf"
                                " INNER JOIN web_app_products wap ON waf.prod_substitute_id = wap.id"
                                " LEFT JOIN web_app_products as sp ON waf.prod_substitute_id = sp.id WHERE user_id = %s", (curr_id, ))

    return render(request, "web_app/favorites.html", locals())


def delete_prod(request):
    deleted = request.GET.get('value')
    id = 'ROFL'
    try:
        fav = Favs.objects.get(prod_id=deleted).delete()
    except Favs.DoesNotExist:
        prod = Favs.objects.get(prod_substitute_id=deleted)  # Getting the line where is locate the sub's id
        product_id = prod.prod_id
        fav = Favs.objects.filter(prod_substitute_id=deleted).update(prod_substitute_id=product_id)

    data = {'respond': id}
    return JsonResponse(data)
