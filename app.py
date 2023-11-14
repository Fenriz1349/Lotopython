# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:21:00 2023

@author: Acerbus
"""
from tkinter import *
from tkinter import ttk
from fonctions import *
import random as rd
import numpy as np
import pandas as pd
from zipfile import ZipFile 
import matplotlib.pyplot as plt
import requests
import os

#suppression des anciennes donnée, importation des nouvelles et création des df de donnée
viderDossierData()
importDatalotoFdj()
importDataEuromillionsFdj()

dataAncien=creationDfAncienLoto('data/LotoAvant2008.csv','data/SuperLotoAvant2008.csv')
dataLoto=creationDfLoto('data/loto2008_2017.csv','data/loto2017_2019.csv','data/loto2019.csv','data/loto2019_now.csv',
                           'data/GrandLoto2019_now.csv','data/lotoNoel2017_now.csv','data/SuperLoto2008_2017.csv','data/SuperLoto2017_2019.csv',
                           'data/SuperLoto2019_now.csv')
dataLotoTotal=pd.concat([dataAncien,dataLoto],ignore_index=True).sort_values(by='annee_numero_de_tirage')
dataEuromillions=creationDfEuromllions('data/euromillions2004_2011.csv','data/euromillions2011_2014.csv', 'data/euromillions2014_2016.csv',
                                          'data/euromillions2016_2019.csv', 'data/euromillions2019_2020.csv', 'data/euromillions2020_now.csv')
dicoOccurences=generateurDicoOccurences(dataLotoTotal)
dicoOccurencesBonus=generateurDicoOccurencesBonus(dataLotoTotal)
dicoOccurencesComplementaire=generateurDicoOccurencesComplementaire(dataAncien)
dicoOccurencesEuro=generateurDicoOccurences(dataEuromillions)
dicoOccurencesEuroEtoiles=generateurDicoOccurencesEtoiles(dataEuromillions)
#calculate pour chaque bouton 
def calculateLotoRandom():
    try:
        tirage=""
        liste =tirageAleatoireUnique(dataLoto)
        for i in liste[0:-1]:
            tirage+=str(i)+" "
        lotoRnd.set(tirage.strip())
        lotoRndBonus.set(str(liste[-1]))
    except ValueError:
        pass
def calculateLotoMoinsCourant():
    try:
        tirage=""
        liste =lotoMoinsRecurent(dicoOccurences,dicoOccurencesBonus)
        for i in liste[0:-1]:
            tirage+=str(i)+" "
        lotoMoins.set(tirage.strip())
        lotoMoinsBonus.set(str(liste[-1]))
    except ValueError:
        pass
def calculateLotoPlusCourant():
    try:
        tirage=""
        liste =lotoPlusRecurent(dicoOccurences,dicoOccurencesBonus)
        for i in liste[0:-1]:
            tirage+=str(i)+" "
        lotoPlus.set(tirage.strip())
        lotoPlusBonus.set(str(liste[-1]))
    except ValueError:
        pass
def calculateEuroRandom():
    try:
        tirage=""
        liste =tirageEuroAleatoireUnique(dataEuromillions)
        for i in liste[0:-2]:
            tirage+=str(i)+" "
        EuroRnd.set(tirage.strip())
        EuroRndEtoiles.set(str(liste[-2])+" "+str(liste[-1]))
    except ValueError:
        pass
def calculateEuroMoinsCourant():
    try:
        tirage=""
        liste =EuroMoinsRecurent(dicoOccurencesEuro,dicoOccurencesEuroEtoiles)
        for i in liste[0:-2]:
            tirage+=str(i)+" "
        EuroMoins.set(tirage.strip())
        EuroMoinsEtoiles.set(str(liste[-2])+" "+str(liste[-1]))
    except ValueError:
        pass
def calculateEuroPlusCourant():
    try:
        tirage=""
        liste =EuroPlusRecurent(dicoOccurencesEuro,dicoOccurencesEuroEtoiles)
        for i in liste[0:-2]:
            tirage+=str(i)+" "
        EuroPlus.set(tirage.strip())
        EuroPlusEtoiles.set(str(liste[-2])+" "+str(liste[-1]))
    except ValueError:
        pass
    
#mainframe qui lance toutes les fonctions
root = Tk()
root.title("Generateur de Loto et Euromillions")


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#labels des tirages
ttk.Label(mainframe, text="Loto").grid(column=0, row=0, sticky=E)
ttk.Label(mainframe, text="Tirage").grid(column=1, row=0)
ttk.Label(mainframe, text="N° bonus").grid(column=2, row=0)
ttk.Label(mainframe, text="Aléatoire").grid(column=0, row=1, sticky=E)
ttk.Label(mainframe, text="les moins courant").grid(column=0, row=2, sticky=E)
ttk.Label(mainframe, text="les plus courant").grid(column=0, row=3, sticky=E)
ttk.Label(mainframe, text="Euromillions").grid(column=0, row=4, sticky=E)
ttk.Label(mainframe, text="Tirage").grid(column=1, row=4)
ttk.Label(mainframe, text="Etoiles bonus").grid(column=2, row=4)
ttk.Label(mainframe, text="Aléatoire").grid(column=0, row=5, sticky=E)
ttk.Label(mainframe, text="les moins courant").grid(column=0, row=6, sticky=E)
ttk.Label(mainframe, text="les plus courant").grid(column=0, row=7, sticky=E)
#champs pour chaque tirages
lotoRnd = StringVar()
ttk.Label(mainframe, textvariable=lotoRnd).grid(column=1, row=1, sticky=(E))
lotoRndBonus = StringVar()
ttk.Label(mainframe, textvariable=lotoRndBonus).grid(column=2, row=1, sticky=(W))

lotoMoins = StringVar()
ttk.Label(mainframe, textvariable=lotoMoins).grid(column=1, row=2, sticky=(E))
lotoMoinsBonus = StringVar()
ttk.Label(mainframe, textvariable=lotoMoinsBonus).grid(column=2, row=2, sticky=(W))

lotoPlus = StringVar()
ttk.Label(mainframe, textvariable=lotoPlus).grid(column=1, row=3, sticky=(E))
lotoPlusBonus = StringVar()
ttk.Label(mainframe, textvariable=lotoPlusBonus).grid(column=2, row=3, sticky=(W))

EuroRnd = StringVar()
ttk.Label(mainframe, textvariable=EuroRnd).grid(column=1, row=5, sticky=(E))
EuroRndEtoiles = StringVar()
ttk.Label(mainframe, textvariable=EuroRndEtoiles).grid(column=2, row=5, sticky=(W))

EuroMoins = StringVar()
ttk.Label(mainframe, textvariable=EuroMoins).grid(column=1, row=6, sticky=(E))
EuroMoinsEtoiles = StringVar()
ttk.Label(mainframe, textvariable=EuroMoinsEtoiles).grid(column=2, row=6, sticky=(W))

EuroPlus = StringVar()
ttk.Label(mainframe, textvariable=EuroPlus).grid(column=1, row=7, sticky=(E))
EuroPlusEtoiles = StringVar()
ttk.Label(mainframe, textvariable=EuroPlusEtoiles).grid(column=2, row=7, sticky=(W))

#Boutons pour chaque fonctions
ttk.Button(mainframe, text="lancer", command=calculateLotoRandom).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="lancer", command=calculateLotoMoinsCourant).grid(column=3, row=2, sticky=W)
ttk.Button(mainframe, text="lancer", command=calculateLotoPlusCourant).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="lancer", command=calculateEuroRandom).grid(column=3, row=5, sticky=W)
ttk.Button(mainframe, text="lancer", command=calculateEuroMoinsCourant).grid(column=3, row=6, sticky=W)
ttk.Button(mainframe, text="lancer", command=calculateEuroPlusCourant).grid(column=3, row=7, sticky=W)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)


root.mainloop()