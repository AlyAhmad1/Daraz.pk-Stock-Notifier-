from django.urls import path
from . import views
D = views.Scrap()

urlpatterns = [
    path('', D.Daraz, name='Home'),
    path('About', D.About, name='About'),
    path('Help', D.Help, name='Help'),
]
