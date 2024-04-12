from django.db import models
from django.db.models import F
from monsite import settings
from datetime import datetime

# Create your models here.

class Declenchement(models.Model):
    #question_text = models.CharField(max_length=200)
    #pub_date = models.DateTimeField("date published")

    Cust_Code = models.CharField(max_length=20)
    TYPE_DECLEN = models.CharField(max_length=10)
    #DATE = models.DateField()	
    DATE = models.CharField(max_length=10)
    H_RECEPT = models.TimeField()	
    H_DESPATCH	= models.TimeField(blank=True, null = True, )
    H_ARRIVEE	= models.TimeField(blank=True, null = True)
    CODE = models.CharField(max_length=50, blank=True, null = True)
    EQUIPAGE = models.TextField(blank=True, null = True)
    NOM_CLIENT	 = models.TextField()
    ADRESSE_CLIENT = models.TextField(blank=True, null = True)	
    COMMENTAIRE	= models.TextField(blank=True, null = True)
    TEMPS_INTER = models.TimeField(blank=True, null = True)	
    TEMPS_PATRL	= models.TimeField(blank=True, null = True)
    TEMPS_PRONTO = models.TimeField(blank=True, null = True)

    class Meta:
        ordering = ['NOM_CLIENT'] 

    def __str__(self):
        return '%s %s' % (self.NOM_CLIENT, self.ADRESSE_CLIENT)



class Coordonnee(models.Model):
    Cust_Code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    Nom = models.TextField(blank=True, null = True)
    Adresse = models.TextField(blank=True, null = True)

    class Meta:
        ordering = ['Nom'] 

    def __str__(self):
        return '%s %s' % (self.Nom, self.Adresse) 



class Dispatch_Engin(models.Model):
    Vehicule = models.TextField()
    Area = models.TextField()
    Description = models.TextField()

    def __str__(self):
        return self.Description 
    

class Formulaire(models.Model):    
    date_heure = models.DateTimeField()
    