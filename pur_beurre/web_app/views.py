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
        if form.is_valid():  # If the search form is valid, search for the product and display the results
            product = form.cleaned_data['research']
            return redirect('results/' + product + '/')
        else:
            form = SearchForm()
            form_nav = SearchForm_NavBar()

    else:
        form = SearchForm()
        form_nav = SearchForm_NavBar()  # Display a search bar inside de navbar
        return render(request, "web_app/index.html", locals())


def legals(request):  # Display legal notice

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


def register(request):  # Route to the register page

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():  # If all fields are complete then register the user with values of each field
            username = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            return redirect('../login/')  # And redirect him to the login page

        else:
            pass

    else:
        form = RegisterForm()

    return render(request, "web_app/register.html", locals())


def login(request):  # Login page
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:  # If the auth didn't return an error, log the user
                log(request, user)
                return redirect('../index/')  # And redirect him to the index page
            else:
                pass
        else:
            pass
    else:
        form = LoginForm()

    return render(request, "web_app/connexion.html", locals())


def logout(request):  # Logout function
    out(request)
    return redirect('../login/')  # Once the user has been logged out redirect him into the login page


@login_required
def my_account(request):  # Display the account's page

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


def results(request, product):  # Display the result of the search function

    if request.method == 'POST':
        form_nav = SearchForm_NavBar(request.POST)
        if form.is_valid():
            product = form.cleaned_data['research']
            return redirect('result/' + product + '/')
        else:
            form_nav = SearchForm_NavBar()
    else:
        form_nav = SearchForm_NavBar()
    # Search for every product that contains words searched by the user
    prods = Products.objects.raw("SELECT * FROM web_app_products WHERE name LIKE %(p)s ORDER by grade ASC", {"p": "%{}%"
                                 .format(product.replace(' ', '%'))})

    try:
        # Check if the user entered the precise name of a product
        searched = get_object_or_404(Products, name__icontains=product)

    except MultipleObjectsReturned:
        # If the product is registered multiple time, display only one
        searched = Products.objects.filter(name__icontains=product).first()

    return render(request, "web_app/results.html", locals())


def details(request, product):  # Display the details of a selected product

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


def my_favs(request):  # Display the saved products of an user

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
    #  Select all products from the prod_id's column

    test_prods = Products.objects.raw("SELECT p.name AS prod_name, p.grade AS prod_grade, p.id AS produ_id,"
                                      " p.img_url as img, sp.img_url as image, p.grade as grade,"
                                      " sp.grade as nutriscore, sp.name AS sub_name,"
                                      " sp.id AS sub_prod_id, waf.id"
                                      " FROM web_app_favs waf"
                                      " INNER JOIN web_app_products p ON waf.prod_id = p.id"
                                      " LEFT JOIN web_app_products sp ON waf.prod_substitute_id = sp.id WHERE user_id = %s", (curr_id, ))

    return render(request, "web_app/favorites.html", locals())


def delete_prod(request):
    deleted = request.GET.get('value')
    sub_id = request.GET.get('value_2')

    id = "Done"

    try:

        if sub_id:

            Favs.objects.filter(prod_id=deleted, prod_substitute_id=sub_id).delete()
        else:
            Favs.objects.filter(prod_id=deleted)[1].delete()

    except IndexError:
        prod = Favs.objects.filter(prod_substitute_id=deleted).first()
        product_id = prod.prod_id
        Favs.objects.filter(prod_substitute_id=deleted).update(prod_substitute_id=product_id)
    except Favs.DoesNotExist:
        prod = Favs.objects.get(prod_substitute_id=deleted)  # Getting the line where is locate the sub's id
        product_id = prod.prod_id
        Favs.objects.filter(prod_substitute_id=deleted).update(prod_substitute_id=product_id)
    except Favs.MultipleObjectsReturned:
        pass

    data = {'respond': id}
    return JsonResponse(data)
