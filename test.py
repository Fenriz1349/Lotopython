# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:32:12 2023

@author: Acerbus
"""

import random as rd
import numpy as np
import pandas as pd
from zipfile import ZipFile 
import matplotlib.pyplot as plt
import requests
import os
import fonctions as fc


def main():
    '''fc.viderDossierData()
    fc.importDatalotoFdj()
    fc.importDataEuromillionsFdj()'''
    
    dataAncien=fc.creationDfAncienLoto('data/LotoAvant2008.csv','data/SuperLotoAvant2008.csv')
    dataLoto=fc.creationDfLoto('data/loto2008_2017.csv','data/loto2017_2019.csv','data/loto2019.csv','data/loto2019_now.csv',
                               'data/GrandLoto2019_now.csv','data/lotoNoel2017_now.csv','data/SuperLoto2008_2017.csv','data/SuperLoto2017_2019.csv',
                               'data/SuperLoto2019_now.csv')
    dataLotoTotal=pd.concat([dataAncien,dataLoto],ignore_index=True).sort_values(by='annee_numero_de_tirage')
    dataEuromillions=fc.creationDfEuromllions('data/euromillions2004_2011.csv','data/euromillions2011_2014.csv', 'data/euromillions2014_2016.csv',
                                              'data/euromillions2016_2019.csv', 'data/euromillions2019_2020.csv', 'data/euromillions2020_now.csv')
    '''print(dataAncien.columns)
    print(dataLoto.columns)
    print(dataLotoTotal.columns)'''
    #print(dataEuromillions['date_de_tirage'])

    dicoOccurences=fc.generateurDicoOccurences(dataLotoTotal)
    #print(dict(sorted(dicoOccurences.items(), key=lambda item:item[1], reverse=True)))
    dicoOccurencesBonus=fc.generateurDicoOccurencesBonus(dataLotoTotal)
    #print(dict(sorted(dicoOccurencesBonus.items(), key=lambda item:item[1], reverse=True)))
    dicoOccurencesComplementaire=fc.generateurDicoOccurencesComplementaire(dataAncien)
    #print(dict(sorted(dicoOccurencesComplementaire.items(), key=lambda item:item[1], reverse=True)))
    dicoOccurencesEuro=fc.generateurDicoOccurences(dataEuromillions)
    #print(dict(sorted(dicoOccurencesEuro.items(), key=lambda item:item[1], reverse=True)))
    dicoOccurencesEuroEtoiles=fc.generateurDicoOccurencesEtoiles(dataEuromillions)
    #print(dicoOccurencesEuroEtoiles)
    tirage=fc.tirageAleatoireUnique(dataLoto)
    tirageMoinsCourant=fc.lotoMoinsRecurent(dicoOccurences,dicoOccurencesBonus)
    tiragePlusCourant=fc.lotoPlusRecurent(dicoOccurences,dicoOccurencesBonus)
    tirageEuro=fc.tirageEuroAleatoireUnique(dataEuromillions)
    tirageEuroMoins=fc.EuroMoinsRecurent(dicoOccurencesEuro, dicoOccurencesEuroEtoiles)
    #print(tirageEuroMoins)
    tirageEuroPlus=fc.EuroPlusRecurent(dicoOccurencesEuro, dicoOccurencesEuroEtoiles)
    #print(tirageEuroPlus)
    
    '''dfJourSemaineAvant2008=fc.DfNbGagnant(dataAncien)
    dfJourSemaineDepuis2008=fc.DfNbGagnant(dataLoto)
    dfJourSemaineLotoTotal=fc.DfNbGagnant(dataLotoTotal)
    dfJourSemaineEuromillions=fc.DfNbGagnant(dataEuromillions)
    #print(dfJourSemaine)'''
    
    '''fc.PieNbGagnantTotal(dfJourSemaineAvant2008,'Nombre moyen de gagnant au rang 1 par jour de tirage entre 1976 et 2008')
    fc.PieNbGagnantTotal(dfJourSemaineDepuis2008,'Nombre moyen de gagnant au rang 1 par jour de tirage depuis 2008')
    fc.PieNbGagnantTotal(dfJourSemaineLotoTotal,'Nombre moyen de gagnant au rang 1 par jour de tirage depuis 1976')
    fc.PieNbGagnantTotal(dfJourSemaineEuromillions,'Nombre moyen de gagnant à l\'Euromillions au rang 1 par jour de tirage depuis 2004')
    
    fc.BarNbGagnantAnnee(dfJourSemaineAvant2008,'Nombre moyen de gagnant du rang 1 au Loto par année entre 1976 et 2008 par jour de tirage')
    fc.BarNbGagnantAnnee(dfJourSemaineDepuis2008,'Nombre moyen de gagnant du rang 1 au Loto par année depuis 2008 par jour de tirage')
    fc.BarNbGagnantAnnee(dfJourSemaineLotoTotal,'Nombre moyen de gagnant du rang 1 au Loto par année depuis 1976 par jour de tirage')
    fc.BarNbGagnantAnnee(dfJourSemaineEuromillions,'Nombre moyen de gagnant du rang 1 àl\'Euromillions par année depuis 2004 par jour de tirage')'''
    
    dfJourSemaineMillionAvant2008=fc.DfMillion(dataAncien)
    '''dfJourSemaineMillionDepuis2008=fc.DfMillion(dataLoto)
    dfJourSemaineMillionTotal=fc.DfMillion(dataLotoTotal)
    dfJourSemaineMillionEuromillions=fc.DfMillion(dataEuromillions)   
    
    fc.PieMillionMoyen(dfJourSemaineMillionAvant2008,'gain moyen du rang 1 par jour de tirage entre 1976 et 2008')
    fc.PieMillionMoyen(dfJourSemaineMillionDepuis2008,'gain moyen du rang 1 par jour de tirage depuis 2008')
    fc.PieMillionMoyen(dfJourSemaineMillionTotal,'gain moyen du rang 1 par jour de tirage depuis 1976')
   # fc.PieMillionMoyen(dfJourSemaineMillionEuromillions,'gain moyen du rang 1 à l\'Euromillions par jour de tirage depuis 2004')'''

    ''''fc.BarMillionMoyen(dfJourSemaineMillion)'''
    
main()