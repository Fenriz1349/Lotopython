# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:23:15 2023

@author: Acerbus
"""
import random as rd
import numpy as np
import pandas as pd
from zipfile import ZipFile 
import matplotlib.pyplot as plt
import requests
import os
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

dicoConversionJour={'LU':'lundi','MA':'mardi','ME':'mercredi','JE':'jeudi','VE':'vendredi','SA':'samedi'}

dicoColonneEuro={'nombre_de_gagnant_au_rang1_Euro_Millions_en_france':'nombre_de_gagnant_au_rang1_en_france',
                 'nombre_de_gagnant_au_rang1_Euro_Millions_en_europe':'nombre_de_gagnant_au_rang1_en_europe',
                 'rapport_du_rang1_Euro_Millions':'rapport_du_rang1',
                 'nombre_de_gagnant_au_rang2_Euro_Millions_en_france':'nombre_de_gagnant_au_rang2_en_france',
                 'nombre_de_gagnant_au_rang2_Euro_Millions_en_europe':'nombre_de_gagnant_au_rang2_en_europe',
                 'rapport_du_rang2_Euro_Millions':'rapport_du_rang2'}

'''fonction pour vider le dossier data avant un nouvel export'''
def viderDossierData():
    for files in os.listdir('data'):
        os.remove('data/'+files)
'''fonction pour récuperer les fichier zip des tirages du loto sur le site fdj, extraire et renommer les csv dans un dossier data'''
def importDatalotoFdj():
    dicoUrlLoto={
    'URLavant2008' : "https://media.fdj.fr/static-draws/csv/loto/loto_197605.zip",
    'URL2008_2017' : "https://media.fdj.fr/static-draws/csv/loto/loto_200810.zip",
    'URL2017_2019' : "https://media.fdj.fr/static-draws/csv/loto/loto_201703.zip",
    'URL2019' : "https://media.fdj.fr/static-draws/csv/loto/loto_201902.zip",
    'URL2019_now' : "https://media.fdj.fr/static-draws/csv/loto/loto_201911.zip",
    'URLSuperavant2008' : "https://media.fdj.fr/static-draws/csv/loto/superloto_199605.zip",
    'URLSuper2008_2017' : "https://media.fdj.fr/static-draws/csv/loto/superloto_200810.zip",
    'URLSuper2017_2019' : 'https://media.fdj.fr/static-draws/csv/loto/superloto_201703.zip',
    'URLSuper2019_now' : 'https://media.fdj.fr/static-draws/csv/loto/superloto_201907.zip',
    'URLnoel2017_now': 'https://media.fdj.fr/static-draws/csv/loto/lotonoel_201703.zip',
    'URLGrandLoto2019_now': 'https://media.fdj.fr/static-draws/csv/loto/grandloto_201912.zip'}
    nomLotoCSV={
        'LotoAvant2008.csv' : 'loto.csv',
        'loto2008_2017.csv' :'nouveau_loto.csv' ,
        'loto2017_2019.csv' : 'loto2017.csv',
        'loto2019.csv' : 'loto_201902.csv',
        'loto2019_now.csv' :'loto_201911.csv' ,
        'SuperLotoAvant2008.csv' : 'sloto.csv',
        'SuperLoto2008_2017.csv' : 'nouveau_superloto.csv',
        'SuperLoto2017_2019.csv' : 'superloto2017.csv',
        'SuperLoto2019_now.csv' :'superloto_201907.csv' ,
        'lotoNoel2017_now.csv': 'lotonoel2017.csv',
        'GrandLoto2019_now.csv':'grandloto_201912.csv'}
    
    for i in dicoUrlLoto:
        response = requests.get(dicoUrlLoto[i])
        file=dicoUrlLoto[i][dicoUrlLoto[i].rfind('/')+1:]
        open(file,"wb").write(response.content)
        with ZipFile(file, 'r') as zip: 
            zip.extractall('data')
        os.remove(file)
    for i in nomLotoCSV:
        os.renames('data/'+nomLotoCSV[i],'data/'+i)

'''fonction pour recuperer les fichier zip de l'euromillion sur le site fdj, extraire et renommer les fichier csv dans un dossier data'''
def importDataEuromillionsFdj():
    dicoUrlEuromillions={
    'URL2004_2011' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_200402.zip',
    'URL2011_2014' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201105.zip',
    'URL2014_2016' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201402.zip',
    'URL2016_2019' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201609.zip',
    'URL2019_2020' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201902.zip',
    'URL2020_now' : 'https://media.fdj.fr/static-draws/csv/euromillions/euromillions_202002.zip',}
    nomEuroCSV={
        'euromillions2004_2011.csv' :'euromillions.csv' ,
        'euromillions2011_2014.csv' : 'euromillions_2.csv',
        'euromillions2014_2016.csv' : 'euromillions_3.csv',
        'euromillions2016_2019.csv' : 'euromillions_4.csv',
        'euromillions2019_2020.csv' : 'euromillions_201902.csv',
        'euromillions2020_now.csv' :'euromillions_202002.csv'}
    
    
    for i in dicoUrlEuromillions:
        response = requests.get(dicoUrlEuromillions[i])
        file=dicoUrlEuromillions[i][dicoUrlEuromillions[i].rfind('/')+1:]
        open(file,"wb").write(response.content)
        with ZipFile(file, 'r') as zip: 
            zip.extractall('data')
        os.remove(file)
    for i in nomEuroCSV:
        os.renames('data/'+nomEuroCSV[i],'data/'+i)
        
'''fonction qui prend en parametre les csv d\'avant 2008 et renvoie un data frame propre rangé par date'''
def creationDfAncienLoto(file,filesuper):
    data = pd.read_csv(file,delimiter=';',quotechar='"',encoding='latin-1')
    datasuper = pd.read_csv(filesuper,delimiter=';',quotechar='"',encoding='latin-1')
    data=data.drop(columns =['1er_ou_2eme_tirage','date_de_forclusion','nombre_de_gagnant_au_rang3', 'rapport_du_rang3','nombre_de_gagnant_au_rang4',
                             'rapport_du_rang4','nombre_de_gagnant_au_rang5', 'rapport_du_rang5','nombre_de_gagnant_au_rang6', 'rapport_du_rang6',
                             'nombre_de_gagnant_au_rang7', 'rapport_du_rang7','numero_joker','numero_jokerplus'])
    datasuper=datasuper.drop(columns=['date_de_forclusion','nombre_de_gagnant_au_rang3', 'rapport_du_rang3','nombre_de_gagnant_au_rang4','rapport_du_rang4',
                                      'nombre_de_gagnant_au_rang5','rapport_du_rang5','nombre_de_gagnant_au_rang6','rapport_du_rang6',
                                      'nombre_de_gagnant_au_rang7','rapport_du_rang7','numero_jokerplus'])
    dataAncien=pd.concat([data,datasuper],ignore_index=True)
    dataAncien=dataAncien.drop(columns=['Unnamed: 30','Unnamed: 28'])
    dataAncien['jour_de_tirage']=dataAncien['jour_de_tirage'].map(dicoConversionJour)
    dataAncien['date_de_tirage']=dataAncien['date_de_tirage'].map(lambda i:str(i)[6:8]+'/'+str(i)[4:6]+'/'+str(i)[0:4])
    return (dataAncien.sort_values(by='annee_numero_de_tirage'))

'''recuperer la liste des precedents loto et renvoie un data frame avec le tirage rangé dans l\'ordre dans la colonne tirage'''
def creationDfLoto(loto2008_2017,loto2017_2019,loto2019,loto2019_now,GrandLoto2019_now,lotoNoel2017_now,SuperLoto2008_2017,SuperLoto2017_2019,SuperLoto2019_now):
    df2008_2017 = pd.read_csv(loto2008_2017,delimiter=';',quotechar='"',encoding='latin-1')
    df2017_2019 = pd.read_csv(loto2017_2019,delimiter=';',quotechar='"',encoding='latin-1')
    df2019 = pd.read_csv(loto2019,delimiter=';',quotechar='"',encoding='latin-1')
    df2019_now = pd.read_csv(loto2019_now,delimiter=';',quotechar='"',encoding='latin-1')
    dfGrnadLoto2019_now = pd.read_csv(GrandLoto2019_now,delimiter=';',quotechar='"',encoding='latin-1')
    dfNoel2017_now = pd.read_csv(lotoNoel2017_now,delimiter=';',quotechar='"',encoding='latin-1')
    dfSuperLoto2008_2017 = pd.read_csv(SuperLoto2008_2017,delimiter=';',quotechar='"',encoding='latin-1')
    dfSuperLoto2017_2019 = pd.read_csv(SuperLoto2017_2019,delimiter=';',quotechar='"',encoding='latin-1')
    dfSuperLoto2019_now = pd.read_csv(SuperLoto2019_now,delimiter=';',quotechar='"',encoding='latin-1')
    
    liste1=['date_de_forclusion','nombre_de_gagnant_au_rang3','rapport_du_rang3','nombre_de_gagnant_au_rang4','rapport_du_rang4',
            'nombre_de_gagnant_au_rang5','rapport_du_rang5','nombre_de_gagnant_au_rang6', 'rapport_du_rang6','numero_jokerplus','Unnamed: 25']
    liste2=['date_de_forclusion','nombre_de_gagnant_au_rang3', 'rapport_du_rang3','nombre_de_gagnant_au_rang4','rapport_du_rang4','nombre_de_gagnant_au_rang5',
            'rapport_du_rang5','nombre_de_gagnant_au_rang6', 'rapport_du_rang6','nombre_de_gagnant_au_rang7', 'rapport_du_rang7','nombre_de_gagnant_au_rang8',
            'rapport_du_rang8','nombre_de_gagnant_au_rang9', 'rapport_du_rang9','nombre_de_codes_gagnants', 'rapport_codes_gagnants','codes_gagnants','numero_jokerplus','Unnamed: 34']
    liste3=['date_de_forclusion','nombre_de_gagnant_au_rang3', 'rapport_du_rang3','nombre_de_gagnant_au_rang4','rapport_du_rang4','nombre_de_gagnant_au_rang5', 
            'rapport_du_rang5','nombre_de_gagnant_au_rang6', 'rapport_du_rang6','nombre_de_gagnant_au_rang7','rapport_du_rang7','nombre_de_gagnant_au_rang8',
            'rapport_du_rang8','nombre_de_gagnant_au_rang9', 'rapport_du_rang9','nombre_de_codes_gagnants', 'rapport_codes_gagnants', 'codes_gagnants',
            'boule_1_second_tirage', 'boule_2_second_tirage','boule_3_second_tirage', 'boule_4_second_tirage','boule_5_second_tirage', 'promotion_second_tirage',
            'combinaison_gagnant_second_tirage_en_ordre_croissant','nombre_de_gagnant_au_rang_1_second_tirage','rapport_du_rang1_second_tirage','nombre_de_gagnant_au_rang_2_second_tirage',
            'rapport_du_rang2_second_tirage','nombre_de_gagnant_au_rang_3_second_tirage','rapport_du_rang3_second_tirage','nombre_de_gagnant_au_rang_4_second_tirage',
            'rapport_du_rang4_second_tirage', 'numero_jokerplus','Unnamed: 49']
    
    df2008_2017=df2008_2017.drop(columns=liste1)
    df2017_2019=df2017_2019.drop(columns=liste2)
    df2019=df2019.drop(columns =liste2)
    df2019_now=df2019_now.drop(columns =liste3)
    dfGrnadLoto2019_now=dfGrnadLoto2019_now.drop(columns =liste2)
    dfNoel2017_now=dfNoel2017_now.drop(columns =liste2)
    dfSuperLoto2008_2017=dfSuperLoto2008_2017.drop(columns =liste1)
    dfSuperLoto2017_2019=dfSuperLoto2017_2019.drop(columns =liste2)
    dfSuperLoto2019_now=dfSuperLoto2019_now.drop(columns =liste2)

    dataloto=pd.concat([df2008_2017,df2017_2019,df2019,df2019_now,dfGrnadLoto2019_now,dfNoel2017_now,dfSuperLoto2008_2017,dfSuperLoto2017_2019,dfSuperLoto2019_now],ignore_index=True)
    dataloto['jour_de_tirage']=dataloto['jour_de_tirage'].str.lower().str.strip()
    return (dataloto.sort_values(by='annee_numero_de_tirage'))

'''fonction qui prend en parametre les csv de l'euromillions et renvoie un data frame propre rangé par date'''
def creationDfEuromllions(euromillions2004_2011,euromillions2011_2014,euromillions2014_2016,euromillions2016_2019,euromillions2019_2020,euromillions2020_now):
    dfeuromillions2004_2011 = pd.read_csv(euromillions2004_2011,delimiter=';',quotechar='"',encoding='latin-1')
    dfeuromillions2011_2014 = pd.read_csv(euromillions2011_2014,delimiter=';',quotechar='"',encoding='latin-1')
    dfeuromillions2014_2016 = pd.read_csv(euromillions2014_2016,delimiter=';',quotechar='"',encoding='latin-1')
    dfeuromillions2016_2019 = pd.read_csv(euromillions2016_2019,delimiter=';',quotechar='"',encoding='latin-1')
    dfeuromillions2016_2019=dfeuromillions2016_2019.shift(periods=1,axis=1)
    dfeuromillions2016_2019['annee_numero_de_tirage']=dfeuromillions2016_2019.index
    dfeuromillions2019_2020 = pd.read_csv(euromillions2019_2020,delimiter=';',quotechar='"',encoding='latin-1')
    dfeuromillions2020_now = pd.read_csv(euromillions2020_now,delimiter=';',quotechar='"',encoding='latin-1')
    
    liste1=['date_de_forclusion','nombre_de_gagnant_au_rang3_en_france','nombre_de_gagnant_au_rang3_en_europe',
            'rapport_du_rang3','nombre_de_gagnant_au_rang4_en_france','nombre_de_gagnant_au_rang4_en_europe','rapport_du_rang4','nombre_de_gagnant_au_rang5_en_france',
            'nombre_de_gagnant_au_rang5_en_europe','rapport_du_rang5','nombre_de_gagnant_au_rang6_en_france','nombre_de_gagnant_au_rang6_en_europe',
            'rapport_du_rang6','nombre_de_gagnant_au_rang7_en_france','nombre_de_gagnant_au_rang7_en_europe','rapport_du_rang7','nombre_de_gagnant_au_rang8_en_france',
            'nombre_de_gagnant_au_rang8_en_europe','rapport_du_rang8','nombre_de_gagnant_au_rang9_en_france','nombre_de_gagnant_au_rang9_en_europe', 'rapport_du_rang9',
            'nombre_de_gagnant_au_rang10_en_france','nombre_de_gagnant_au_rang10_en_europe','rapport_du_rang10','nombre_de_gagnant_au_rang11_en_france',
            'nombre_de_gagnant_au_rang11_en_europe','rapport_du_rang11','nombre_de_gagnant_au_rang12_en_france','nombre_de_gagnant_au_rang12_en_europe',
            'rapport_du_rang12','numero_jokerplus','Unnamed: 51']
    liste2=['date_de_forclusion','nombre_de_gagnant_au_rang3_en_france','nombre_de_gagnant_au_rang3_en_europe',
            'rapport_du_rang3','nombre_de_gagnant_au_rang4_en_france','nombre_de_gagnant_au_rang4_en_europe','rapport_du_rang4','nombre_de_gagnant_au_rang5_en_france',
            'nombre_de_gagnant_au_rang5_en_europe','rapport_du_rang5','nombre_de_gagnant_au_rang6_en_france','nombre_de_gagnant_au_rang6_en_europe',
            'rapport_du_rang6','nombre_de_gagnant_au_rang7_en_france','nombre_de_gagnant_au_rang7_en_europe','rapport_du_rang7','nombre_de_gagnant_au_rang8_en_france',
            'nombre_de_gagnant_au_rang8_en_europe','rapport_du_rang8','nombre_de_gagnant_au_rang9_en_france','nombre_de_gagnant_au_rang9_en_europe', 'rapport_du_rang9',
            'nombre_de_gagnant_au_rang10_en_france','nombre_de_gagnant_au_rang10_en_europe','rapport_du_rang10','nombre_de_gagnant_au_rang11_en_france',
            'nombre_de_gagnant_au_rang11_en_europe','rapport_du_rang11','nombre_de_gagnant_au_rang12_en_france','nombre_de_gagnant_au_rang12_en_europe',
            'rapport_du_rang12','nombre_de_gagnant_au_rang13_en_france','nombre_de_gagnant_au_rang13_en_europe', 'rapport_du_rang13','numero_jokerplus','Unnamed: 54']
    liste3=['numéro_de_tirage_dans_le_cycle', 'date_de_forclusion','nombre_de_gagnant_au_rang3_Euro_Millions_en_france','nombre_de_gagnant_au_rang3_Euro_Millions_en_europe',
            'rapport_du_rang3_Euro_Millions','nombre_de_gagnant_au_rang4_Euro_Millions_en_france','nombre_de_gagnant_au_rang4_Euro_Millions_en_europe',
            'rapport_du_rang4_Euro_Millions','nombre_de_gagnant_au_rang5_Euro_Millions_en_france','nombre_de_gagnant_au_rang5_Euro_Millions_en_europe',
            'rapport_du_rang5_Euro_Millions','nombre_de_gagnant_au_rang6_Euro_Millions_en_france','nombre_de_gagnant_au_rang6_Euro_Millions_en_europe',
            'rapport_du_rang6_Euro_Millions','nombre_de_gagnant_au_rang7_Euro_Millions_en_france','nombre_de_gagnant_au_rang7_Euro_Millions_en_europe',
            'rapport_du_rang7_Euro_Millions','nombre_de_gagnant_au_rang8_Euro_Millions_en_france','nombre_de_gagnant_au_rang8_Euro_Millions_en_europe',
            'rapport_du_rang8_Euro_Millions','nombre_de_gagnant_au_rang9_Euro_Millions_en_france','nombre_de_gagnant_au_rang9_Euro_Millions_en_europe',
            'rapport_du_rang9_Euro_Millions','nombre_de_gagnant_au_rang10_Euro_Millions_en_france','nombre_de_gagnant_au_rang10_Euro_Millions_en_europe',
            'rapport_du_rang10_Euro_Millions','nombre_de_gagnant_au_rang11_Euro_Millions_en_france','nombre_de_gagnant_au_rang11_Euro_Millions_en_europe',
            'rapport_du_rang11_Euro_Millions','nombre_de_gagnant_au_rang12_Euro_Millions_en_france','nombre_de_gagnant_au_rang12_Euro_Millions_en_europe',
            'rapport_du_rang12_Euro_Millions','nombre_de_gagnant_au_rang13_Euro_Millions_en_france','nombre_de_gagnant_au_rang13_Euro_Millions_en_europe',
            'rapport_du_rang13_Euro_Millions','nombre_de_gagnant_au_rang1_Etoile+','rapport_du_rang1_Etoile+','nombre_de_gagnant_au_rang2_Etoile+',
            'rapport_du_rang2_Etoile+','nombre_de_gagnant_au_rang3_Etoile+','rapport_du_rang3_Etoile+', 'nombre_de_gagnant_au_rang4_Etoile+',
            'rapport_du_rang4_Etoile+','nombre_de_gagnant_au_rang5_Etoile+','rapport_du_rang5_Etoile+','nombre_de_gagnant_au_rang6_Etoile+','rapport_du_rang6_Etoile+',
            'nombre_de_gagnant_au_rang7_Etoile+','rapport_du_rang7_Etoile+','nombre_de_gagnant_au_rang8_Etoile+','rapport_du_rang8_Etoile+',
            'nombre_de_gagnant_au_rang9_Etoile+','rapport_du_rang9_Etoile+','nombre_de_gagnant_au_rang10_Etoile+','rapport_du_rang10_Etoile+','numero_My_Million',
            'numero_Tirage_Exceptionnel_Euro_Millions']
    liste4=liste3[0:-1]+['numero_Tirage_Exceptionnel_Euro_Million']
    
    dfeuromillions2004_2011=dfeuromillions2004_2011.drop(columns=liste1)
    dfeuromillions2004_2011['jour_de_tirage']=dfeuromillions2004_2011['jour_de_tirage'].map(dicoConversionJour)
    dfeuromillions2004_2011['date_de_tirage']=str(dfeuromillions2004_2011['date_de_tirage'].values[0])[-2:]+'/'+str(dfeuromillions2004_2011['date_de_tirage'].values[0])[4:6]+'/'+str(dfeuromillions2004_2011['date_de_tirage'].values[0])[0:4]
    
    dfeuromillions2011_2014=dfeuromillions2011_2014.drop(columns=liste2)
    
    dfeuromillions2014_2016=dfeuromillions2014_2016.drop(columns=liste2[:34]+liste2[35:]+['numero_My_Million'])
    
    dfeuromillions2016_2019=dfeuromillions2016_2019.drop(columns=liste3)
    dfeuromillions2016_2019.rename(columns=dicoColonneEuro,inplace=True)
    dfeuromillions2016_2019['devise']='eur'
    
    dfeuromillions2019_2020=dfeuromillions2019_2020.drop(columns =liste4+['Unnamed: 75'])
    dfeuromillions2019_2020.rename(columns=dicoColonneEuro,inplace=True)
    dfeuromillions2019_2020['devise']='eur'
    
    dfeuromillions2020_now=dfeuromillions2020_now.drop(columns =liste4+['Unnamed: 75'])
    dfeuromillions2020_now.rename(columns=dicoColonneEuro,inplace=True)
    dfeuromillions2020_now['devise']='eur'
    
    dataEuro=pd.concat([dfeuromillions2004_2011,dfeuromillions2011_2014,dfeuromillions2014_2016,dfeuromillions2016_2019,dfeuromillions2019_2020,dfeuromillions2020_now],ignore_index=True)
    dataEuro['jour_de_tirage']=dataEuro['jour_de_tirage'].str.lower().str.strip()
    dataEuro['rapport_du_rang1']=dataEuro['rapport_du_rang1'].apply(lambda x:int(x))
    dataEuro['boules_gagnantes_en_ordre_croissant']=dataEuro['boules_gagnantes_en_ordre_croissant'][1:-1]
    dataEuro['etoiles_gagnantes_en_ordre_croissant']=dataEuro['etoiles_gagnantes_en_ordre_croissant'][1:-1]
    return (dataEuro.sort_values(by='annee_numero_de_tirage'))

'''fonction qui créé un dictionnaire avec les occurences de chaque numero pour tous les tirages
prend en parametre un dataframe et renvoie un dictionnaire'''
def generateurDicoOccurences(data):
    dico={}
    n=1
    colonne='boule_'+str(n)
    while colonne in data.columns:
        for i in data[colonne].values:
            if i in dico:dico[i]+=1
            elif not math.isnan(i) :dico[i]=1
        n+=1
        colonne='boule_'+str(n)
    return dict(sorted(dico.items()))

'''fonction qui créé un dictionnaire avec les occurences de chaque bonus pour tous les tirages
prend en parametre un dataframe et renvoie un dictionnaire'''
def generateurDicoOccurencesBonus(data):
    dicoBonus={}
    for i in data['numero_chance'].values:
        if i in dicoBonus:dicoBonus[i]+=1
        elif not math.isnan(i):dicoBonus[int(i)]=1
    return dict(sorted(dicoBonus.items()))
'''fonction qui créé un dictionnaire avec les occurences des numeros complementaire pour tous les tirages
prend en parametre un dataframe et renvoie un dictionnaire'''
def generateurDicoOccurencesComplementaire(data):
    dicoBonus={}
    for i in data['boule_complementaire'].values:
        if i in dicoBonus:dicoBonus[i]+=1
        elif not math.isnan(i):dicoBonus[i]=1
    return dict(sorted(dicoBonus.items()))

'''fonction qui créé un dictionnaire avec les occurences des étoiles pour tous les tirages
prend en parametre un dataframe et renvoie un dictionnaire'''
def generateurDicoOccurencesEtoiles(data):
    dicoEtoile={}
    n=1
    colonne='etoile_'+str(n)
    while colonne in data.columns:
        for i in data[colonne].values:
            if i in dicoEtoile:dicoEtoile[i]+=1
            else :dicoEtoile[i]=1
        n+=1
        colonne='etoile_'+str(n)
    return dict(sorted(dicoEtoile.items()))

'''un generateur de loto qui n'est jamais tombées,les 5 nombres et le bonus à la fin
prend en parametre un dataframe et renvoie une liste'''
def tirageAleatoireUnique(data):
    while True:
        liste=[]
        for i in range(5):
            while True :
                num=rd.randint(1, 49)
                if num not in liste :
                    liste.append(num)
                    break
                else :continue
        liste.sort()
        liste.append(rd.randint(1, 10))
        test=str(liste[0])+'-'+str(liste[1])+'-'+str(liste[2])+'-'+str(liste[3])+'-'+str(liste[4])+'+'+str(liste[5])
        if  len(data.loc[data['combinaison_gagnante_en_ordre_croissant']==test])==0:
            return liste
            break
        else: continue

'''un generateur de Loto qui prend les 5 numeros qui tombent le moins et le bonus qui tombe le moins
prend en parametre un dataframe et renvoie une liste'''
def lotoMoinsRecurent(dicoOccu,dicoBonus):
    dicoOccurencesMoins=dict(sorted(dicoOccu.items(), key=lambda item:item[1])).copy()
    bonus=sorted(dicoBonus.items(), key=lambda item:item[1])[0][0]
    liste=[]
    for i in dicoOccurencesMoins.keys():
        if len(liste)<5:
            liste.append(i)
        else :break
    liste.append(bonus)
    return liste

'''un generateur de Loto qui prend les 5 numeros qui tombent le plus et le bonus qui tombe le plus
prend en parametre un dataframe et renvoie une liste'''
def lotoPlusRecurent(dicoOccu,dicoBonus):
    dicoOccurencesPlus=dict(sorted(dicoOccu.items(), key=lambda item:item[1], reverse=True)).copy()
    bonus=sorted(dicoBonus.items(), key=lambda item:item[1],reverse=True)[0][0]
    liste=[]
    for i in dicoOccurencesPlus.keys():
        if len(liste)<5:
            liste.append(i)
        else :break
    liste.append(bonus)
    return liste

'''un generateur de Euromillions qui n'est jamais tombées,les 5 nombres et le bonus à la fin
prend en parametre un dataframe et renvoie une liste'''
def tirageEuroAleatoireUnique(data):
    while True:
        liste=[]
        for i in range(5):
            while True :
                num=rd.randint(1,50)
                if num not in liste :
                    liste.append(num)
                    break
                else :continue
        liste.sort()
        etoile=[]
        for i in range(2):
            while True :
                num=rd.randint(1,12)
                if num not in etoile :
                    etoile.append(num)
                    break
                else :continue
        etoile.sort()
        test=str(liste[0])+'-'+str(liste[1])+'-'+str(liste[2])+'-'+str(liste[3])+'-'+str(liste[4])
        etoiletest=str(etoile[0])+'-'+str(etoile[1])
        if  len(data.loc[data['boules_gagnantes_en_ordre_croissant']==test])==0 and len(data.loc[data['etoiles_gagnantes_en_ordre_croissant']==etoiletest])==0:
            return liste+etoile
            break
        else: continue

'''un generateur de Euromillions qui prend les 5 numeros qui tombent le moins et les 2 étoiles qui tombe le moins
prend en parametre un dataframe et renvoie une liste'''
def EuroMoinsRecurent(dicoOccu,dicoEtoile):
    dicoOccurencesMoins=dict(sorted(dicoOccu.items(), key=lambda item:item[1])).copy()
    dicoEtoile=dict(sorted(dicoEtoile.items(), key=lambda item:item[1])).copy()
    liste=[]
    for i in dicoOccurencesMoins.keys():
        if len(liste)<5:
            liste.append(i)
        else :break
    etoile=[]
    for i in dicoEtoile.keys():
        if len(etoile)<2:
            etoile.append(i)
        else :break
    return liste+etoile

'''un generateur de Euromillions qui prend les 5 numeros qui tombent le plus et les 2 étoiles qui tombe le plus
prend en parametre un dataframe et renvoie une liste'''
def EuroPlusRecurent(dicoOccu,dicoEtoile):
    dicoOccurencesMoins=dict(sorted(dicoOccu.items(), key=lambda item:item[1],reverse=True)).copy()
    dicoEtoile=dict(sorted(dicoEtoile.items(), key=lambda item:item[1],reverse=True)).copy()
    liste=[]
    for i in dicoOccurencesMoins.keys():
        if len(liste)<5:
            liste.append(i)
        else :break
    etoile=[]
    for i in dicoEtoile.keys():
        if len(etoile)<2:
            etoile.append(i)
        else :break
    return liste+etoile

'''fonction pour ajouter des etiquettes de données sur les histogrammes'''
def ajouterEtiquetteValeur(x_list, y_list):
    for i in range(1, len(x_list) + 1):
        plt.text(i, y_list[i - 1], y_list[i - 1], ha="center")

'''fonction qui prend 1 à plusieurs df et qui retourne le nombre de gaagnants par jour de tirage cumulé puis par année'''
def DfNbGagnant(*data):
    dfJourSemaine=pd.DataFrame()
    for i in data:
        dataN=i.copy()
        if 'nombre_de_gagnant_au_rang1_en_europe' in dataN.columns:
            dataN=dataN.rename(columns={'nombre_de_gagnant_au_rang1_en_europe':'nombre_de_gagnant_au_rang1'})
        dataN=dataN[['jour_de_tirage','date_de_tirage','nombre_de_gagnant_au_rang1']]
        dfJourSemaine=pd.concat([dfJourSemaine,dataN],ignore_index=True)
    dfJourSemaine['date_de_tirage']=dfJourSemaine['date_de_tirage'].apply(lambda x:x[-4:])
    for i in dfJourSemaine['date_de_tirage']:
        if i=='9/16':i='2016'
    dfJourSemaine=dfJourSemaine.rename(columns={'date_de_tirage':'annee'}).sort_values(by='jour_de_tirage')
    return dfJourSemaine.sort_values(by='annee')

'''fonction qui prend 1  plusieurs dataframe et renvoie un df avec le gain max moyen par jour de tirage, et gain moyen tous rangs confondus '''
def DfMillion(data):
    dfJourSemaineMillion=data.copy()
    
    if 'nombre_de_gagnant_au_rang1_en_europe' in dfJourSemaineMillion.columns:
        dfJourSemaineMillion=dfJourSemaineMillion.rename(columns={'nombre_de_gagnant_au_rang1_en_europe':'nombre_de_gagnant_au_rang1'})
    dfJourSemaineMillion=dfJourSemaineMillion[['jour_de_tirage','date_de_tirage','nombre_de_gagnant_au_rang1','rapport_du_rang1']]
    '''for i in dfJourSemaineMillion['rapport_du_rang1'].values[0]:
        if i[-2]=='+' and type(i)==str:
            if i[-1]=='6':
                n=i[0]+'.'+i[2:4]
                i=float(n)
            elif i[-1]=='7':
                n=i[0:2]+'.'+i[3]
                i=float(n)
        else :i=float(i)/1000000'''
    
    dfJourSemaineMillion['date_de_tirage']=dfJourSemaineMillion['date_de_tirage'].apply(lambda x:x[-4:])
    #for i in dfJourSemaineMillion['rapport_du_rang1']:
     #   if type(i)!=int:print(i)
    dfJourSemaineMillion['rapport_du_rang1']=dfJourSemaineMillion['rapport_du_rang1'].apply(lambda x:int(x))
    dfJourSemaineMillion=dfJourSemaineMillion.rename(columns={'date_de_tirage':'annee'}).sort_values(by='annee')
    dfJourSemaineMillion['annee'].tail(1).values[0]='2016'
    dfJourSemaineMillion=dfJourSemaineMillion.loc[dfJourSemaineMillion['nombre_de_gagnant_au_rang1']>0]
    return dfJourSemaineMillion.sort_values(by='annee')

'''calcul toutes années cummulées'''
def PieNbGagnantTotal(data,titre):
    nbGagnant=data['nombre_de_gagnant_au_rang1'].sum()
    dfJourSemaineCum=pd.pivot_table(data[['jour_de_tirage','nombre_de_gagnant_au_rang1']],columns='jour_de_tirage',values='nombre_de_gagnant_au_rang1',aggfunc='mean').reset_index()
    dfJourSemaineCum=pd.melt(dfJourSemaineCum,id_vars='index')
    columns=['nombre_de_gagnant_au_rang1']
    rows=[]
    for i in dfJourSemaineCum['jour_de_tirage']:
        rows.append(i)
    cell_text=[]
    for row in range(len(data)):
        cell_text.append([])
    figure = Figure(figsize=(4,3), dpi=100)
    subplot = figure.add_subplot(111)
    subplot.plt.pie(data=dfJourSemaineCum,
            x='value',
            labels='jour_de_tirage',
            autopct=lambda i:round(i,2),
            #explode=(beat == max(beat) * 0.1),
            shadow=True)
    plt.table(cellText=cell_text,
              rowLabels=rows,
              colLabels=columns,
              loc='bottom')
    plt.title(titre)

'''calcul pour chaque année'''
def BarNbGagnantAnnee(data,titre):
    dfJourSemaineNbGagnant=pd.pivot_table(data,index='annee',columns='jour_de_tirage',values='nombre_de_gagnant_au_rang1',aggfunc='sum').reset_index()
    
    dfJourSemaineNbGagnant.plot(x='annee', 
            kind='bar', 
            stacked=False, 
            figsize=(25,10),
            title=titre,
            width=0.8,
            ylabel='nombre de gagnants',
            xlabel='années')
            #,yticks=np.arange(0, 22, 2)))
    plt.show()
    
'''calcul du gain max par jour cumulé '''
def PieMillionMoyen(data,titre):
    '''nbGagnant=data['nombre_de_gagnant_au_rang1'].sum()
    gainMoyenTotal=(int(data['rapport_du_rang1'])//100).sum()//nbGagnant'''
    dfJourSemaineMillionTotal=pd.pivot_table(data,columns='jour_de_tirage',values='rapport_du_rang1',aggfunc='mean').reset_index()
    dfJourSemaineMillionTotal=pd.melt(dfJourSemaineMillionTotal,id_vars='index')
    print(dfJourSemaineMillionTotal)
    for i in dfJourSemaineMillionTotal['annee']:
        if i=='9/16':i='2016'
    plt.pie(data=dfJourSemaineMillionTotal,
            x='value',
            labels='jour_de_tirage',
            autopct=lambda i:'{:,}'.format(i),
            #explode=(0,0,0.15),
            shadow=True)
    plt.title(titre)
    plt.show()

'''calcul pour chaque année '''
def BarMillionMoyen(data,titre):
    dfJourSemaineMillionAnnee=pd.pivot_table(data,index='annee',columns='jour_de_tirage',values='rapport_du_rang1',aggfunc='mean').reset_index()
    
    dfJourSemaineMillionAnnee.plot(x='annee', 
            kind='bar', 
            stacked=False, 
            figsize=(25,10),
            title='gain moyen du rang 1 au Loto par année et par jour de tirage',
            width=0.8,
            ylabel='gain en millions d''€',
            xlabel='années',
            yticks=np.arange(0, 10000000, 1000000))
    plt.show()
