from django.urls import path
from . import views

app_name = "web_app"
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('mon_compte/', views.my_account, name='my_account'),
    path('results/<product>/', views.results, name='results'),
    path('details/<product>/', views.details, name='details'),
    path('test/', views.test, name='test')

]

