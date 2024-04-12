from django.urls import path
from . import views


app_name = 'carte'

urlpatterns = [

    # Accueil
    path('', views.accueil, name='accueil'), 

    # Mise à jour des données
    path('update', views.Mise_a_jour, name='update'), 

    # Carte 
    path('carte', views.carte, name='carte'),

    # Actualise la Carte 
    path('carte_actualise_htmx/<str:pk1>/<str:pk2>/<str:pk3>/<str:pk4>', views.carte_actualise_htmx, name='carte_actualise_htmx'),

    # Contact 
    path('contact', views.contact, name='contact'), 

     ]