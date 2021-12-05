from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.inedx,name = 'main'),
    path('about',views.about , name='about'),
    path('pass',views.pass_data , name ='pass'),
]