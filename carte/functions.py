import pandas as pd
from datetime import datetime
from .models import Dispatch_Engin

# Champ à ajouter : Cust Code

def rapport_alarme (ma_base) :
                
    ma_base['filtre'] = ma_base.Notepad.str[9:14] 
    ma_base['filtre'] = ma_base['filtre'].str.replace('ALARM','ALARME')

    def ma_selection(ma_base) : 
        if (ma_base['filtre'].find("PANIC") == 0) or (ma_base['filtre'].find("ALARM") == 0) : 
            return "ok" 
        else : 
            return "no"

    ma_base["test"] = ma_base.apply(ma_selection, axis=1)

    selection = ma_base.loc[(ma_base['test'] == 'ok')]
    ma_base = selection
	
    ### Je selectionne uniquement les alarmes (Type : alarme et panic) ici : 
                
    ####################### DEBUT TRAITEMENT DE LA BASE SELECTION OU MA_BASE Vehicle
                               
    #OPERATEUR = selection["Operator"] 
    TYPE_DECLENCHEMENT = selection["filtre"]
    CODE_ALARME = selection["Xmit"]
    COMMENTAIRE = selection["Notepad"]
    EQUIPAGE = selection["Vehicle"]   
    Cust_Code = selection["Cust Code"]              
    #TEMPS_PRONTO 

    date_et_heure = list(map(lambda x: x.partition(".")[0], selection["Signal Time"].astype(str)))
    #date_et_heure

    # DATE_ET_HEURE = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), date_et_heure))

    DATE = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y'), date_et_heure))
    DATE_ET_HEURE = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'), date_et_heure)) # A modifier

    H_RECEPT = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S').time(), date_et_heure))

    # FONCTION HEURE 
    def heure(value_1) :
        if value_1 == 'NaT' : return "" 
        else : return datetime.strptime(str(value_1), '%Y-%m-%d %H:%M:%S').time()

    # HEURE DE DESPATCH 
    desp = list(map(lambda x: x.partition(".")[0], selection["Despatch"].astype(str))) 
    db_desp = pd.DataFrame(desp, columns=["Desp"],)
    H_DESPATCH = db_desp.apply(lambda x: heure(x["Desp"]), axis=1)

    # HEURE D'ARRIVEE 
    arr = list(map(lambda x: x.partition(".")[0], selection["Arrived"].astype(str)))
    db_arr = pd.DataFrame(arr, columns=["Arr"],)
    H_ARRIVEE = db_arr.apply(lambda x: heure(x["Arr"]), axis=1)
            
    # FONCTION TEMPS : PATRL + INTERVENTION 
    def temps(val) : 
        val = str(val) 
        if val == 'nan' : return ""
        else : return val
                
    # Temps d'intervention (Heure d'arrivée de la patrouille - Heure de reception du signal)
    inter,  = selection["Sig-Arr Time"],
    db_inter,  = pd.DataFrame(list(inter), columns=["inter"],), 
    TEMPS_INTER,  = db_inter.apply(lambda x: temps(x["inter"]), axis=1),
                
    # Temps Patrouille : temps mis par la patrouille pour arriver chez le client dès que Pronto leur a donné l'alerte 
    patrl = selection["Des-ArrTime"]
    db_patrl = pd.DataFrame(list(patrl), columns=["patrl"],)
    TEMPS_PATRL = db_patrl.apply(lambda x: temps(x["patrl"]), axis=1)

    #  Temps mis par pronto pour lancer un équipage dès la reception du signal 
    ### FONCTION PRONTO : Je calcule le temps de PRONTO
    def pronto(val_1, val_2) :
        val_2, val_1 = str(val_2), str(val_1)
        if (val_1 =="") or (val_2 =="") or (val_1 =="NaT") or (val_2 =="NaT") :
            return ""
        else :
            format = "%H:%M:%S"
            val_2 = datetime.strptime(val_2, format)
            val_1 = datetime.strptime(val_1, format)
            val = val_2 - val_1
            val = datetime.strptime(str(val), format).time()
            return val

    # Temps Pronto : temps mis par Pronto pour lancer la patrouille dès la reception du code
    db_pronto = pd.DataFrame(list(zip(TEMPS_PATRL, TEMPS_INTER)), columns=["patrl", "inter"],)
    TEMPS_PRONTO = db_pronto.apply(lambda x: pronto(x["patrl"], x["inter"]), axis=1)
                
    ## Ajouter l'équipage après le code de l'alarme : 
    equipe = pd.DataFrame(list(EQUIPAGE), columns=["Area"]) 
    equipe_test = equipe['Area'].astype(str)
    equipe_test = equipe_test.str.replace("nan", "Richard")
    equipe = pd.DataFrame(list(equipe_test), columns=["Area"])
  
    colonne = [{"Area": x.Area, "Vehicule": x.Vehicule, "Description": x.Description} for x in Dispatch_Engin.objects.all()]
    mes_equipe = pd.DataFrame(colonne)

    fusion_equipe = equipe.merge(mes_equipe, how='left', on='Area')

    fusion_equipe_fin = fusion_equipe['Description'].astype(str)
    fusion_equipe_fin = fusion_equipe_fin.str.replace("nan", "")

    ############################################## RESULTAT ET AFFICHAGE  ###################################################
    resultat = pd.DataFrame(list(zip(Cust_Code, TYPE_DECLENCHEMENT, DATE_ET_HEURE, DATE, H_RECEPT, H_DESPATCH, H_ARRIVEE, CODE_ALARME, fusion_equipe_fin,    
                                            selection["custdesc"], selection["PhysicalAddress"],COMMENTAIRE, TEMPS_INTER,  
                                            TEMPS_PATRL, TEMPS_PRONTO)), 

                                    columns=["Cust_Code","TYPE_DECLEN", "DATE_ET_HEURE", "DATE", "H_RECEPT", "H_DESPATCH", "H_ARRIVEE", "CODE","EQUIPAGE", 
                                             "NOM_CLIENT", "ADRESSE_CLIENT", "COMMENTAIRE", "TEMPS_INTER",  "TEMPS_PATRL", "TEMPS_PRONTO"])
    return resultat

 