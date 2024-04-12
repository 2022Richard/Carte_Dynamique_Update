from django.contrib import admin


# Register your models here.


from carte.models import *


class Affiche_Declenchement (admin.ModelAdmin):
    #add_fieldsets = ('classe','parent_eleve', 'date_de_naissance')
    list_display = ('Cust_Code', 'TYPE_DECLEN', 'DATE', 'H_RECEPT', 'CODE', 'NOM_CLIENT','ADRESSE_CLIENT')


class Affiche_Coordonnees_GPS (admin.ModelAdmin):
    #add_fieldsets = ('classe','parent_eleve', 'date_de_naissance')
    list_display = ('Cust_Code', 'latitude', 'longitude')



#admin.site.register(Personne)
#admin.site.register(Declenchement, Affiche_Declenchement)

#admin.site.register(Coordonnee, Affiche_Coordonnees_GPS)



class AdminDispatch_Engin (admin.ModelAdmin):
    list_display = ('Vehicule', 'Area', 'Description')  

from import_export.admin import ImportExportModelAdmin 

@admin.register(Dispatch_Engin)
class ViewAdmin (ImportExportModelAdmin) : 
    pass

@admin.register(Declenchement)
class ViewAdmin (ImportExportModelAdmin) : 
    pass

@admin.register(Coordonnee)
class ViewAdmin (ImportExportModelAdmin) : 
    pass