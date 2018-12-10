from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=125)


class Products(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    store = models.CharField(max_length=60)
    grade = models.CharField(max_length=1)
    kj_100g = models.IntegerField()
    cat_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    proteins_100g = models.FloatField()
    sugars_100g = models.FloatField()
    fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()


class Favs(models.Model):
    prod_id = models.IntegerField()
    prod_substitute_id = models.IntegerField()
    user_id = models.IntegerField()






