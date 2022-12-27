import os, os.path, random, glob, csv, subprocess
import streamlit as st
import numpy as np
import pandas as pd



def recupTitre():
    titre=""
    titre = st.text_input(" Nom de l'évaluation : ", value="Évaluation de mathématiques", max_chars = 40, help="Tapez votre titre",)
    return titre

def choixNiveau():
    choix = st.radio('CHOIX DU NIVEAU', ('6e', '5e', '4e', '3e', 'Autre'))
    if choix == 'Autre':
        choix2 = st.text_input(" Niveau : ", value="", max_chars = 10, help="Tapez votre niveau",)
        return choix2
    else :
        return choix

def choixClasse():
    choix = st.radio('CHOIX DU NOM', (' A', ' B', ' C', ' D', ' Autre'))
    if choix == ' Autre':
        choix2 = st.text_input(" Nom de la classe : ", value="", max_chars = 15, help="Tapez votre nom de classe",)
        return " "+choix2
    else :
        return choix

def choixDate() :
    return st.date_input(" Date de l'éval : ", help="Entrez la date de l'évaluation des élèves. ")


def recupEtab() :
    
    return st.text_input(" Nom de l'établissement : ", value="Collège Coat Mez de Daoulas", max_chars = 35, help = "Tapez le nom de l'établissement",)



def recupDemandes() :
    
    fichierdemandes = st.file_uploader("Fichier demandes.csv de SACoche")

    sep=";"
    sep = st.radio('CHOIX DU SEPARATEUR CSV', (';', ',', 'une tabulation', 'un espace'), horizontal = True) 

    if sep == 'un espace' :
        sep = ' '
    if sep =='une tabulation' :
        sep = '    '

    if fichierdemandes is not None and fichierdemandes.name[-4:] == ".csv" :
        
        st.success("Fichier bien reçu !")
        dataframe_demandes = pd.read_csv(fichierdemandes, sep)
        st.write(dataframe_demandes)
        return dataframe_demandes
        
    else :
        if fichierdemandes is not None :
            st.error("Erreur, cela ne semble pas être un fichier csv. Chargez un autre fichier SVP")
        return None


def recupTex(cle) :
    
    fichierTex = st.file_uploader("Fichier Communs.tex contenant les exercices", key=str(cle+random.random()))

    if fichierTex is not None and fichierTex.name[-4:] == ".tex" :

        st.success("Fichier bien reçu !")
        
    else :
        if fichierTex is not None :
            st.error("Erreur, cela ne semble pas être un fichier tex. Chargez un autre fichier SVP")
    return fichierTex


def interfaceGraphique1():
     
    st.write("""

    ##### 1. Entrer ici le titre de l'évaluation :
    """)

    titre = recupTitre()

    if titre != "":
        st.write(""" _Titre de l'évaluation :_ """, titre)

    st.write(""" 
    ##### 2. Choisir la classe évaluée :

    """)

    col1, col2 = st.columns(2)

    with col1:
        
        niveau = choixNiveau()

    with col2:
        classe =  choixClasse()

    classe = niveau + classe
    st.write('_La classe est :_ ', classe)


    st.write(""" 
    ##### 3. Entrer ici la date de l'évaluation :

    """)

    date = choixDate()

    if date != "":
        st.write(""" _La date de l'évaluation est le :_ """, date.strftime("%d/%m/%Y"))
        
        
    st.write(""" 
    ##### 4. Entrer ici le nom de l'établissement :

    """)
    
    etab = recupEtab()
        
    return (etab, titre, date.strftime("%d/%m/%Y"), classe)

def recupNom():
    titre = st.text_input(" Nom du fichier : ", value="evalALaCarte", key = 1, max_chars = 30, help="Tapez votre nom de fichier.",)
    return titre
    
def OuiNon():
    if st.radio('VOTRE REPONSE', ('Non', 'Oui'), horizontal = True ) =="Oui" :
        return "o"
    else :
        return "n"

def OuiNon2():
    if st.radio('VOTRE REPONSE', (' Non', ' Oui'), horizontal = True) ==" Oui" :
        return "o"
    else :
        return "n"
    
def OuiNon3():
    if st.radio('VOTRE REPONSE', ('Non', ' Oui'), horizontal = True) ==" Oui" :
        return "o"
    else :
        return "n"


def interfaceGraphique2():

    st.write("""

    ##### 5. Entrer ici le nom (sans l'extension) du fichier $\LaTeX$ qui sera créé :
    """)

    nom_fichier_eval = recupNom()+".tex"

    if nom_fichier_eval != "":
        st.write(""" _Nom du fichier créé :_ """, nom_fichier_eval)

    st.write(""" 
    ##### 6. Voulez-vous ajouter un ou des exercices communs à tous les élèves ?

    """)
    
    exosCommuns = OuiNon()
    
    if exosCommuns == "o":
        st.write(""" 
        ##### + Voulez-vous aussi un sujet ne contenant que les exercices communs ?
        """)
    
        devoircommun = OuiNon3()
        
    else :
        devoircommun = "n"
        
    
    st.write(""" 
    ##### 7. Voulez-vous ajouter un exercice facultatif à tous les élèves ?

    """)
    
    exoFacultatif = OuiNon2()
    
    return (nom_fichier_eval, exosCommuns, exoFacultatif, devoircommun)
    

