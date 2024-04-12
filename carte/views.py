from django.shortcuts import render
from datetime import datetime
import pandas as pd
from .functions import rapport_alarme
from carte.models import *
from django.contrib import messages
import folium
from folium.plugins import MarkerCluster, Draw
from folium import plugins
from .forms import Formulaire
from django.http import Http404, HttpResponse




# Create your views here. 

def accueil(request): 
    return render(request, 'accueil.html', {'etat':'accueil'})

def contact(request): 
    return render(request, 'contact.html', {'etat':'contact'})

def Mise_a_jour(request): 
    
    if request.method == "POST" : 
        
        file = request.FILES['files']
       
        mon_fichier, test = str(file), False
        type_file = mon_fichier.endswith("xlsx")

        if type_file == False : 
            type_file = mon_fichier.endswith("xls") 

        if type_file == False : 
            messages.error(request,"Ce fichier n'est pas au format excel. Un fichier excel a pour extension xlsx ou xlx. ")
        else : 
            ma_base = pd.read_excel(file)  
            #print( ma_base["Cust Code"] )
            
            if not (("Notepad" in ma_base.columns) or ("Xmit" in ma_base.columns) or ("Despatch" in ma_base.columns) or \
                    ("Vehicle" in ma_base.columns) or ("Arrived" in ma_base.columns) or ("Signal Time" in ma_base.columns) \
                        or ("Sig-Arr Time" in ma_base.columns) or ("Des-ArrTime" in ma_base.columns)) : 
                   
                     messages.error(request,"Ce fichier est au format excel mais pas celui des declenchements alarme.") 
                  
            else :       
                    if not(("custdesc" in ma_base.columns) and ("PhysicalAddress" in ma_base.columns)) :
                    
                        messages.error(request, "Ce fichier est celui des declenchements alarme. \
                               Mais veuillez ajouter les colonnes 'custdesc' et/ou 'PhysicalAddress' puis reessayez !" )
                       
                    else:  test = True
    
            if test == True : 
                # print("to be continued")  

                if 'alarme' in request.POST :  

                    resultat = rapport_alarme(ma_base)  
                    resultat_fin = pd.DataFrame(resultat)
                 
                    res_decl = pd.read_excel("Declenchement.xlsx")
                   
                    frames = [res_decl, resultat_fin]
                    res = pd.concat(frames)

                    duplicate = res[res.duplicated(keep="first")]
                    
                    if duplicate.shape[0] > 0 : 
                        # print("yes")

                         
                        res_clean = res.drop_duplicates()
                       
                        nb_col_clean = res_clean.shape[1] - 15
                        res_clean = res_clean.iloc[:, nb_col_clean :]
                        
                        res_clean.to_excel("Declenchement.xlsx")
                        #print(duplicate) print(res_clean)
                        
                        messages.warning(request, "Mise à jour effectuée avec succès, les doublons ont été supprimés")

                        #print("Yes, présence de doublons")
                    else : 
                        #print("No absence de doublons")     
                        nb_column = res.shape[1] - 15
                        res = res.iloc[:, nb_column :]
                        #print(res)
                        res.to_excel("Declenchement.xlsx")
                       
                        messages.success(request,"Mise à jour effectuée avec succès")
                    
                        
    return render(request, 'mise_a_jour.html', {'etat':'MAP', })       



def carte(request): 

    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=7)
    return render(request, 'carte.html', {'etat':'carte', 'map' : map._repr_html_(), })


def carte_actualise_htmx(request, pk1,pk2,pk3,pk4,) : 
    #choix = str(pk1).strip().strip("*")
    if pk2 > pk1 : 
        heure_fin, heure_debut = pk2, pk1
    elif pk2 == pk1 :
         heure_fin = pk2
         heure_debut = pk1
    else : heure_fin, heure_debut = pk1, pk2   

    if pk4 > pk3 : 
        date_fin, date_debut = pk4, pk3
    elif pk3 == pk4 :
         date_debut = pk4
         date_fin = pk3
    else : date_fin, date_debut = pk3, pk4

   
    df = pd.read_excel("Declenchement.xlsx")
    #df["H_RECEPT"] = pd.to_datetime(df['H_RECEPT'])  # Converti la date au format Y-m-d ou Année, mois, jour
    #print(df.shape)

    format = '%Y-%m-%d'
    date_debut = datetime.strptime(date_debut, format).date()
    date_fin = datetime.strptime(date_fin, format).date()

    df['DATE_ET_HEURE'] = pd.to_datetime(df['DATE_ET_HEURE']) 

    choix_debut = (df['DATE_ET_HEURE'].dt.time >= pd.Timestamp(heure_debut).time()) & \
                    (df['DATE_ET_HEURE'].dt.time <= pd.Timestamp(heure_fin).time()) & (df["DATE_ET_HEURE"].dt.date <= date_fin )  \
                    & (df["DATE_ET_HEURE"].dt.date >= date_debut)
    
    #heure_choix = (df['DATE_ET_HEURE'].dt.time >= pd.Timestamp(heure_debut).time()) & (df['DATE_ET_HEURE'].dt.time <= pd.Timestamp(heure_fin).time())
    choix_fin = df.loc[choix_debut]
    choix_clean = choix_fin
    #print(heure_fin)
    #heure_fin.to_excel("test.xlsx")

    ########################### Mes coordonnées
   
    coordonnees_colonne = [{"Cust_Code": x.Cust_Code, "latitude": x.latitude, "longitude": x.longitude} for x in Coordonnee.objects.all()]
    mes_coordonnees = pd.DataFrame(coordonnees_colonne)
        #print(mes_coordonnees) 

    resultat = pd.merge(choix_clean, mes_coordonnees, on='Cust_Code', how="inner")
        #print(resultat)

    resultat['COMMENTAIRE'] = resultat['COMMENTAIRE'].str.lower() # map(lambda x: x.lower())
    resultat_choix = resultat.query('COMMENTAIRE!="test technique" & COMMENTAIRE!="test technicien"') 

    resultat_choix['NOM_ET_ADRESSE_CLIENT'] = resultat_choix['NOM_CLIENT'].astype(str) + ' ' + resultat_choix['ADRESSE_CLIENT'].astype(str)
   # resultat_choix['DATE'] = pd.to_datetime(df['DATE']).dt.date()
    #resultat_choix['DATE'] = pd.to_datetime(resultat_choix['DATE']).dt.date #, format = '%y%m%d'

    def date_clean(value_1) :
        if value_1 == 'NaT' : return "" 
        else : return datetime.strptime(str(value_1), '%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y')
    #resultat_choix['DATE'] = resultat_choix.apply(lambda x: date_clean(x["DATE"]), axis=1)
    resultat_clean = resultat_choix[['TYPE_DECLEN', 'DATE', 'H_RECEPT', 'CODE', 'NOM_ET_ADRESSE_CLIENT', 'NOM_CLIENT', 'ADRESSE_CLIENT', 'latitude', 'longitude']]
        #print(resultat_clean ['NOM_ET_ADRESSE_CLIENT'])

 ########## Affiche la carte ici
    map = folium.Map((5.37309, -3.99117), tooltip = "G4S Siege" , zoom_start=5)
    cluster = MarkerCluster(name = "Donnees").add_to(map) 

        # Selection des coordonnées pour la carte
    df_map_2 = resultat_clean[['latitude', 'longitude']]

        # Convertir les colonnes en numerique
    df_map_2 = df_map_2.astype({'latitude':'float','longitude':'float'})

    liste = df_map_2.values.tolist()
    liste_taille = len(liste)

    #map = folium.Map(location=[lat_fixe, long_fixe], zoom_start=4)
    for point in range(0, liste_taille) :  
            html = '''
                    <b> Type declench : </b> {} <br>
                    <b> Date : </b> {} <br>
                    <b> Heure : </b>{} <br>
                    <b> Code Alarme : </b>{} <br>
                    
                '''.format(resultat_clean.iloc[point, 0], resultat_clean.iloc[point, 1],resultat_clean.iloc[point, 2], resultat_clean.iloc[point, 3] )
            popup = folium.Popup(html, max_width=1000)
            marker = folium.Marker(liste[point], popup = popup, tooltip = resultat_clean.iloc[point, 4], icon  = folium.Icon(icon = "cloud"))
            marker.add_to(cluster)

    return HttpResponse(f'{map._repr_html_()}') 
    
    
    ##########################"
   

    
