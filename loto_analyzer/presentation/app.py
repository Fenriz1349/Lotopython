# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 08:31:05 2023

@author: Acerbus
"""
from tkinter import *
from tkinter import ttk
from ..fonctions import *
import random as rd
import numpy as np
import pandas as pd
from zipfile import ZipFile 
import matplotlib.pyplot as plt
import requests
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#suppression des anciennes donnée, importation des nouvelles et création des df de donnée
def videEtImporte():
    viderDossierData()
    importDatalotoFdj()
    importDataEuromillionsFdj()
    global dataAncien
    dataAncien=creationDfAncienLoto('data/LotoAvant2008.csv','data/SuperLotoAvant2008.csv')
    global dataLoto
    dataLoto=creationDfLoto('data/loto2008_2017.csv','data/loto2017_2019.csv','data/loto2019.csv','data/loto2019_now.csv',
                                   'data/GrandLoto2019_now.csv','data/lotoNoel2017_now.csv','data/SuperLoto2008_2017.csv','data/SuperLoto2017_2019.csv','data/SuperLoto2019_now.csv')
    global dataLotoTotal
    dataLotoTotal=pd.concat([dataAncien,dataLoto],ignore_index=True).sort_values(by='annee_numero_de_tirage')
    global dataEuromillions
    dataEuromillions=creationDfEuromllions('data/euromillions2004_2011.csv','data/euromillions2011_2014.csv', 'data/euromillions2014_2016.csv',
                                                      'data/euromillions2016_2019.csv', 'data/euromillions2019_2020.csv', 'data/euromillions2020_now.csv')

    global dicoOccurences
    dicoOccurences=generateurDicoOccurences(dataLotoTotal)
    global dicoOccurencesBonus
    dicoOccurencesBonus=generateurDicoOccurencesBonus(dataLotoTotal)
    global  dicoOccurencesComplementaire
    dicoOccurencesComplementaire=generateurDicoOccurencesComplementaire(dataAncien)
    global dicoOccurencesEuro
    dicoOccurencesEuro=generateurDicoOccurences(dataEuromillions)
    global dicoOccurencesEuroEtoiles
    dicoOccurencesEuroEtoiles=generateurDicoOccurencesEtoiles(dataEuromillions)
#fonction calculate pour chaque type de tirages
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
#fonction pour afficher les graphiques


#mainframe qui lance toutes les fonctions
def mainframettk():
    root.title("Generateur de Loto et Euromillions")
    global mainframe
    mainframe=ttk.Panedwindow(root, orient=VERTICAL)
    mainframe.pack(fill="both", expand=True)
    
    global generatorLotoframe
    generatorLotoframe=ttk.Panedwindow(mainframe, orient=HORIZONTAL)
    mainframe.add(generatorLotoframe)
    
    global generatorgraphframe
    generatorgraphframe=ttk.Panedwindow(mainframe, orient=HORIZONTAL)
    mainframe.add(generatorgraphframe)
#bouton d'importation des données
def boutonImporter():
    frameImporter= ttk.Frame(mainframe)
    ttk.Button(frameImporter, text="Importer", command=lambda :videEtImporte()).pack(side="left")
    ttk.Button(frameImporter, text="Quitter", command=lambda :root.destroy()).pack(side="right")
    mainframe.add(frameImporter)
#Frame pour les générateur de lotos
def frameLoto():
    colonnetitrelotoframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonnetitrelotoframe)
    ttk.Label(colonnetitrelotoframe, text="Loto").pack()
    ttk.Label(colonnetitrelotoframe, text="Aléatoire").pack()
    ttk.Label(colonnetitrelotoframe, text="les moins courant").pack()
    ttk.Label(colonnetitrelotoframe, text="les plus courant").pack()
    
    colonnetiragelotoframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonnetiragelotoframe)
    ttk.Label(colonnetiragelotoframe, text="Tirage").pack()
    global lotoRnd 
    lotoRnd= StringVar()
    ttk.Label(colonnetiragelotoframe, textvariable=lotoRnd,width=15).pack()
    global lotoMoins
    lotoMoins= StringVar()
    ttk.Label(colonnetiragelotoframe, textvariable=lotoMoins,width=15).pack()
    global lotoPlus 
    lotoPlus= StringVar()
    ttk.Label(colonnetiragelotoframe, textvariable=lotoPlus,width=15).pack()
    
    colonnebonuslotoframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonnebonuslotoframe)
    ttk.Label(colonnebonuslotoframe, text="N° bonus").pack()
    global lotoRndBonus
    lotoRndBonus = StringVar()
    ttk.Label(colonnebonuslotoframe, textvariable=lotoRndBonus,width=10).pack()
    global lotoMoinsBonus 
    lotoMoinsBonus= StringVar()
    ttk.Label(colonnebonuslotoframe, textvariable=lotoMoinsBonus,width=10).pack()
    global lotoPlusBonus 
    lotoPlusBonus= StringVar()
    ttk.Label(colonnebonuslotoframe, textvariable=lotoPlusBonus,width=10).pack()
    
    colonneboutonlotoframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonneboutonlotoframe)
    ttk.Label(colonneboutonlotoframe, text="").pack()
    ttk.Button(colonneboutonlotoframe, text="lancer", command=lambda :calculateLotoRandom()).pack()
    ttk.Button(colonneboutonlotoframe, text="lancer", command=lambda :calculateLotoMoinsCourant()).pack()
    ttk.Button(colonneboutonlotoframe, text="lancer", command=lambda :calculateLotoPlusCourant()).pack()
#frame pour les générateurs d'Euromillions
def frameEuro():
    colonnetitreEuroframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonnetitreEuroframe)
    ttk.Label(colonnetitreEuroframe, text="Euromillions").pack()
    ttk.Label(colonnetitreEuroframe, text="Aléatoire").pack()
    ttk.Label(colonnetitreEuroframe, text="les moins courant").pack()
    ttk.Label(colonnetitreEuroframe, text="les plus courant").pack()
    
    colonnetirageEuroframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonnetirageEuroframe)
    ttk.Label(colonnetirageEuroframe, text="Tirage").pack()
    global EuroRnd 
    EuroRnd= StringVar()
    ttk.Label(colonnetirageEuroframe, textvariable=EuroRnd,width=15).pack()
    global EuroMoins 
    EuroMoins= StringVar()
    ttk.Label(colonnetirageEuroframe, textvariable=EuroMoins,width=15).pack()
    global EuroPlus 
    EuroPlus= StringVar()
    ttk.Label(colonnetirageEuroframe, textvariable=EuroPlus,width=15).pack()
    
    colonneEtoilesEuroframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonneEtoilesEuroframe)
    ttk.Label(colonneEtoilesEuroframe, text="Etoiles bonus").pack()
    global EuroRndEtoiles 
    EuroRndEtoiles= StringVar()
    ttk.Label(colonneEtoilesEuroframe, textvariable=EuroRndEtoiles,width=10).pack()
    global EuroMoinsEtoiles 
    EuroMoinsEtoiles= StringVar()
    ttk.Label(colonneEtoilesEuroframe, textvariable=EuroMoinsEtoiles,width=10).pack()
    global EuroPlusEtoiles 
    EuroPlusEtoiles= StringVar()
    ttk.Label(colonneEtoilesEuroframe, textvariable=EuroPlusEtoiles,width=10).pack()
    
    colonneboutonEuroframe=ttk.Frame(generatorLotoframe)
    generatorLotoframe.add(colonneboutonEuroframe)
    ttk.Label(colonneboutonEuroframe, text="").pack()
    ttk.Button(colonneboutonEuroframe, text="lancer", command=lambda :calculateEuroRandom()).pack()
    ttk.Button(colonneboutonEuroframe, text="lancer", command=lambda :calculateEuroMoinsCourant()).pack()
    ttk.Button(colonneboutonEuroframe, text="lancer", command=lambda :calculateEuroPlusCourant()).pack()
    
def calculatePieNbGagnantTotal(data,titre):
    t=Toplevel(root)
    t.title(titre)
    dfJourSemaineCum=pd.pivot_table(data[['jour_de_tirage','nombre_de_gagnant_au_rang1']],columns='jour_de_tirage',values='nombre_de_gagnant_au_rang1',aggfunc='mean').reset_index()
    dfJourSemaineCum=pd.melt(dfJourSemaineCum,id_vars='index')
    columns=['nombre_de_gagnant_au_rang1']
    rows=[]
    for i in dfJourSemaineCum['jour_de_tirage']:
        rows.append(i)
    cell_text=[]
    for row in range(len(data)):
        cell_text.append([])
    figure = Figure(figsize=(7,4.5), dpi=100)
    pieCanvas = FigureCanvasTkAgg(figure,master=t)
    subplot = figure.add_subplot()
    subplot.pie(data=dfJourSemaineCum,
            x='value',
            labels='jour_de_tirage',
            autopct=lambda i:round(i,2),
            shadow=True)
    subplot.set_title(titre)
    pieCanvas.get_tk_widget().pack()
    ttk.Button(t, text="Quitter", command=lambda :t.destroy()).pack(side="bottom")
def calculateBarNbGagnantAnnee(data,titre):
    t=Toplevel(root)
    t.title(titre)
    dfJourSemaineNbGagnant=pd.pivot_table(data,index='annee',columns='jour_de_tirage',values='nombre_de_gagnant_au_rang1',aggfunc='sum').reset_index()
    for i in dfJourSemaineNbGagnant['annee']:
        if i=='9/16':i='2016'
    figure = Figure(figsize=(9,5), dpi=100)
    barCanvas = FigureCanvasTkAgg(figure,master=t)
    subplot = figure.add_subplot()
    dfJourSemaineNbGagnant.plot(x='annee', 
            kind='bar', 
            stacked=False, 
            figsize=(25,10),
            title=titre,
            width=1,
            ylabel='nombre de gagnants',
            xlabel='années',
            ax=subplot).grid(axis='y')
    barCanvas.get_tk_widget().pack()
    ttk.Button(t, text="Quitter", command=lambda :t.destroy()).pack(side="bottom")
    
def calculatePieMillionMoyen(data,titre):
    t=Toplevel(root)
    t.title(titre)
    dfJourSemaineMillionTotal=pd.pivot_table(data,columns='jour_de_tirage',values='rapport_du_rang1',aggfunc='mean').reset_index()
    dfJourSemaineMillionTotal=pd.melt(dfJourSemaineMillionTotal,id_vars='index')
    for i in dfJourSemaineMillionTotal['annee']:
        if i=='9/16':i='2016'
    figure = Figure(figsize=(7,4.5), dpi=100)
    pieCanvas = FigureCanvasTkAgg(figure,master=t)
    subplot = figure.add_subplot()
    subplot.pie(data=dfJourSemaineMillionTotal,
            x='value',
            labels='jour_de_tirage',
            autopct=lambda i:'{:,}'.format(i),
            shadow=True)
    subplot.title(titre)
    pieCanvas.get_tk_widget().pack()
    ttk.Button(t, text="Quitter", command=lambda :t.destroy()).pack(side="bottom")
def boutonsAnnee():
    frameListeAnnee=ttk.Labelframe(frameGraphParJour, text="liste des Années",padding="5 10 5 10").grid(column=0,row=6,sticky=NSEW)
    listeAnnee=[]
    for i in pd.unique(dfJourSemaineLotoTotal['annee']):
        listeAnnee.append(str(i))
    checks=[]
    r=6
    c=0
    for i in range(len(listeAnnee)):
        v=StringVar()
        if r<17:r+=1
        else:
            r=7
            c+=1
        check=Checkbutton(frameListeAnnee, text=listeAnnee[i], variable=v)
        check.grid(row=r,column=c)
        v.trace("w", lambda : updateAnneeLoto())
        checks.append((check,v))
    ttk.Label(frameGraphParJour, textvariable="0").grid(column=5, row=6, sticky=(E))
 
def updateAnneeLoto(*args):
    print(v.get())
    liste=[]
    for (check,v) in checks:
        liste.append(v.get())
    print(liste)
    lbl["text"]="zizi"
    
def framegraph():
    #frame pour les graphiques du nombre de gagnant par jour
    global dfJourSemaineLotoTotal
    dfJourSemaineLotoTotal=DfNbGagnant(dataLotoTotal)
    global dfJourSemaineLotoAncien
    dfJourSemaineLotoAncien=DfNbGagnant(dataAncien)
    global dfJourSemaineLoto
    dfJourSemaineLoto=DfNbGagnant(dataLoto)
    global dfJourSemaineEuro
    dfJourSemaineEuro=DfNbGagnant(dataEuromillions)
    '''global dfJourSemaineMillionTotal
    dfJourSemaineMillionTotal=DfMillion(dataLotoTotal)
    global dfJourSemaineMillionAvant2008
    dfJourSemaineMillionAvant2008=DfMillion(dataAncien)
    global dfJourSemaineMillionDepuis2008
    dfJourSemaineMillionDepuis2008=DfMillion(dataLoto)
    global dfJourSemaineMillionEuromillions
    dfJourSemaineMillionEuromillions=DfMillion(dataEuromillions)'''
    
    frameTitreGraph=ttk.Labelframe(generatorgraphframe,text="nombre de gagnant par jour",padding="5 10 5 10")
    generatorgraphframe.add(frameTitreGraph)
    ttk.Label(frameTitreGraph, text='loto de 1976 à aujour\'hui').pack()
    ttk.Label(frameTitreGraph, text='loto de 1976 à 2008').pack()
    ttk.Label(frameTitreGraph, text='loto depuis 2008').pack()
    ttk.Label(frameTitreGraph, text='Euromillion depuis 2011').pack()
    
    framePieMoyenGraph=ttk.Labelframe(generatorgraphframe, text="moyenne par jour",padding="5 10 5 10")
    generatorgraphframe.add(framePieMoyenGraph)
    Button(framePieMoyenGraph, text='Lancer',command=lambda :calculatePieNbGagnantTotal(dfJourSemaineLotoTotal,'Nombre moyen de gagnant au rang 1 par jour de tirage de 1976 à aujour\'hui'),font=('Arial', 8, 'bold')).pack()
    Button(framePieMoyenGraph, text='Lancer',command=lambda :calculatePieNbGagnantTotal(dfJourSemaineLotoAncien,'Nombre moyen de gagnant au rang 1 par jour de tirage de 1976 à 2008 '),font=('Arial', 8, 'bold')).pack()
    Button(framePieMoyenGraph, text='Lancer',command=lambda :calculatePieNbGagnantTotal(dfJourSemaineLoto,'Nombre moyen de gagnant au rang 1 par jour de tirage depuis 2008'),font=('Arial', 8, 'bold')).pack()
    Button(framePieMoyenGraph, text='Lancer',command=lambda :calculatePieNbGagnantTotal(dfJourSemaineEuro,'Nombre moyen de gagnant au rang 1 par jour de tirage d\'Euromillion depuis 2011'),font=('Arial', 8, 'bold')).pack()

    frameBarMoyenGraph=ttk.Labelframe(generatorgraphframe, text="cumulé par an",padding="5 10 5 10")
    generatorgraphframe.add(frameBarMoyenGraph)
    Button(frameBarMoyenGraph, text='Lancer',command=lambda :calculateBarNbGagnantAnnee(dfJourSemaineLotoTotal,'Nombre de gagnant par jour de tirage depuis 1976'),font=('Arial', 8, 'bold')).pack()      
    Button(frameBarMoyenGraph, text='Lancer',command=lambda :calculateBarNbGagnantAnnee(dfJourSemaineLotoAncien,'Nombre de gagnant par jour de tirage entre 1976 et 2008'),font=('Arial', 8, 'bold')).pack()
    Button(frameBarMoyenGraph, text='Lancer',command=lambda :calculateBarNbGagnantAnnee(dfJourSemaineLoto,'Nombre de gagnant par jour de tirage depuis 2008'),font=('Arial', 8, 'bold')).pack()
    Button(frameBarMoyenGraph, text='Lancer',command=lambda :calculateBarNbGagnantAnnee(dfJourSemaineEuro,'Nombre de gagnant par jour de tirage depuis 2011'),font=('Arial', 8, 'bold')).pack()
    
    '''framePieMillionGraph=ttk.Labelframe(generatorgraphframe, text="gain max moyen par jour",padding="5 10 5 10")
    generatorgraphframe.add(framePieMillionGraph)
    Button(framePieMillionGraph, text='Lancer',command=lambda :calculatePieMillionMoyen(dfJourSemaineMillionTotal,'gain moyen du rang 1 par jour de tirage de 1976 à aujour\'hui'),font=('Arial', 8, 'bold')).pack()      
    Button(framePieMillionGraph, text='Lancer',command=lambda :calculatePieMillionMoyen(dfJourSemaineMillionAvant2008,'gain moyen du rang 1 par jour de tirage entre 1976 et 2008'),font=('Arial', 8, 'bold')).pack()
    Button(framePieMillionGraph, text='Lancer',command=lambda :calculatePieMillionMoyen(dfJourSemaineMillionDepuis2008,'gain moyen du rang 1 par jour de tirage depuis 2008'),font=('Arial', 8, 'bold')).pack()
    Button(framePieMillionGraph, text='Lancer',command=lambda :calculatePieMillionMoyen(dfJourSemaineMillionEuromillions,'gain moyen du rang 1 par jour de tirage d\'Euromillion depuis 2011'),font=('Arial', 8, 'bold')).pack()'''

def main(root):
    viderDossierData()
    importDatalotoFdj()
    importDataEuromillionsFdj()
    global dataAncien
    dataAncien=creationDfAncienLoto('data/LotoAvant2008.csv','data/SuperLotoAvant2008.csv')
    global dataLoto
    dataLoto=creationDfLoto('data/loto2008_2017.csv','data/loto2017_2019.csv','data/loto2019.csv','data/loto2019_now.csv',
                                   'data/GrandLoto2019_now.csv','data/lotoNoel2017_now.csv','data/SuperLoto2008_2017.csv','data/SuperLoto2017_2019.csv','data/SuperLoto2019_now.csv')
    global dataLotoTotal
    dataLotoTotal=pd.concat([dataAncien,dataLoto],ignore_index=True).sort_values(by='annee_numero_de_tirage')
    global dataEuromillions
    dataEuromillions=creationDfEuromllions('data/euromillions2004_2011.csv','data/euromillions2011_2014.csv', 'data/euromillions2014_2016.csv',
                                                      'data/euromillions2016_2019.csv', 'data/euromillions2019_2020.csv', 'data/euromillions2020_now.csv')

    global dicoOccurences
    dicoOccurences=generateurDicoOccurences(dataLotoTotal)
    global dicoOccurencesBonus
    dicoOccurencesBonus=generateurDicoOccurencesBonus(dataLotoTotal)
    global  dicoOccurencesComplementaire
    dicoOccurencesComplementaire=generateurDicoOccurencesComplementaire(dataAncien)
    global dicoOccurencesEuro
    dicoOccurencesEuro=generateurDicoOccurences(dataEuromillions)
    global dicoOccurencesEuroEtoiles
    dicoOccurencesEuroEtoiles=generateurDicoOccurencesEtoiles(dataEuromillions)
    
    
    mainframettk()
    boutonImporter()
    frameLoto()
    frameEuro()
    framegraph()
    #boutonsAnnee()
    
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.mainloop()