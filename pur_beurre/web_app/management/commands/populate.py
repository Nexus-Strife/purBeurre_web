from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from web_app.models import Categories
from web_app.models import Products
import psycopg2
import requests
import json
import time
from math import ceil

hostname = 'localhost'
user = 'postgres'
password = 'C1li2tn45!'
database = 'pur_beurre'


class Command(BaseCommand):

    help = "Populate the database, just choose the nbr of cats and products by category you want"

    def handle(self, *args, **options):
        conn = psycopg2.connect(host=hostname, user=user, password=password, database=database)
        cur = conn.cursor()

        print("Veuillez patienter...")
        r = requests.get('https://fr.openfoodfacts.org/categories.json')
        # Using the Requests lib to read the *.json that contain the list of the categories on opendfoodfacts
        categories = r.json()

        nbr_categories = categories["count"]
        nbr_of_cats = int(input("Combien de catégories voulez vous injecter dans la BDD ? "))
        nbr_pages = int(input("Combien de page par catégorie voulez-vous ? "))

        ''' Each 3 next loop ( for ) are used to parse every categories and every pages to add each product in
            the database. '''

        for i in range(nbr_of_cats):
            print(i + 1, " - ", end=" ")
            curr_cat = (categories["tags"][i]["name"])
            print(curr_cat)
            nbr_products = int(categories["tags"][i]["products"])
            nbr_of_pages = ceil(nbr_products / 20)
            print("\t Nombre de produits :", nbr_products, end=" ")
            print("\t Nombre de pages :", nbr_of_pages)
            adresse = categories["tags"][i]["url"] + "/1.json"
            print("\t", adresse)
            cat = Categories(name=curr_cat)
            cat.save()

            for page in range(nbr_pages):
                page = page + 1
                addr = categories["tags"][i]["url"] + "/" + str(page) + ".json"
                p = requests.get(addr)
                products = p.json()

                for Prod in range(20):   # range(20) because there are 20 products per page
                    try:
                        grade_prod = (products["products"][Prod]["nutrition_grades"])
                        store_prod = (products["products"][Prod]["stores"])
                        name_prod = (products["products"][Prod]["product_name"])
                        energy_prod = (products["products"][Prod]["nutriments"]["energy_100g"])
                        url_prod = (products["products"][Prod]["url"])
                        desc_prod = (products["products"][Prod]["generic_name"])
                        img_url = (products["products"][Prod]["image_url"])
                        proteins_100g = (products["products"][Prod]["nutriments"]["proteins_100g"])
                        sugars_100g = (products["products"][Prod]["nutriments"]["sugars_100g"])
                        fat_100g = (products["products"][Prod]["nutriments"]["fat_100g"])
                        salt_100g = (products["products"][Prod]["nutriments"]["salt_100g"])
                        saturated_fat_100g = (products["products"][Prod]["nutriments"]["saturated-fat_100g"])

                        cate_id = Categories.objects.raw("SELECT id FROM web_app_categories WHERE name = %(cats)s", {'cats': curr_cat})[0]

                        # Then replace every blank informations by " unknown "

                        if store_prod == "":
                            store_prod = "Inconnu"
                        elif grade_prod == "":
                            grade_prod = "-"
                        elif energy_prod == "":
                            energy_prod = "Inconnu"
                        elif url_prod == "":
                            url_prod = "Inconnue"
                        elif desc_prod == "":
                            desc_prod = "Non communiquée"

                        #  And add everything into the products table
                        pr = Products(name=name_prod, store=store_prod, grade=grade_prod, kj_100g=energy_prod,  cat_id=cate_id, url=url_prod, description=desc_prod, img_url=img_url, proteins_100g=proteins_100g, sugars_100g=sugars_100g, fat_100g=fat_100g, salt_100g=salt_100g, saturated_fat_100g=saturated_fat_100g)
                        pr.save()

                    except KeyError:
                        continue
            time.sleep(0.1)