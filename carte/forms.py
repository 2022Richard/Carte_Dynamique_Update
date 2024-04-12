from django import forms
from django.forms import ModelForm, fields_for_model
from .models import *




class Formulaire(forms.Form):
    
    #texte = forms.DateTimeField() 
    date_heure= forms.DateField(label = 'Date et heure' ,required=True , widget=forms.DateInput(attrs={'type':'datetime-local', 'class': 'form-control', 'max':datetime.now().date, 'required':''}))
    #Heure = forms.DateTimeInput()
    #class Meta:
     #   model = Formulaire
      #  fields = '__all__'
    