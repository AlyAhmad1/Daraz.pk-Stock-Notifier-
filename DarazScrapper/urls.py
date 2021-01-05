from django.urls import path, include
from . import views
D = views.Scrap()

urlpatterns = [
    path('',D.Daraz, name='Home'),
]
