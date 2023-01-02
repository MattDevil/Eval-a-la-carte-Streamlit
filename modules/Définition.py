import os, os.path, random, glob, csv, subprocess
import streamlit as st
import numpy as np
import pandas as pd



def recupTitre():
    titre=""
    titre = st.text_input(" Nom de l'évaluation : ", value="Évaluation de mathématiques", max_chars = 40, help="Tapez votre titre",label_visibility = "collapsed")
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
    return st.date_input(" Date de l'éval : ", help="Entrez la date de l'évaluation des élèves. ", label_visibility = "collapsed")


def recupEtab() :
    
    return st.text_input(" Nom de l'établissement : ", value="Collège Coat Mez de Daoulas", max_chars = 35, help = "Tapez le nom de l'établissement",label_visibility = "collapsed")

def recupDemandes() :
    fichierdemandes = st.file_uploader("Fichier demandes.csv de SACoche", label_visibility = "collapsed")
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
    
    fichierTex = st.file_uploader("Fichier Communs.tex contenant les exercices", key=str(cle+random.random()), label_visibility = "collapsed")

    if fichierTex is not None and fichierTex.name[-4:] == ".tex" :

        st.success("Fichier bien reçu !")
        return fichierTex
    else :
        if fichierTex is not None :
            st.error("Erreur, cela ne semble pas être un fichier tex. Chargez un autre fichier SVP")
        return None

def recupTex1() :
    
    fichierTex = st.file_uploader("Fichier Communs.tex contenant les exercices", label_visibility = "collapsed")

    if fichierTex is not None and fichierTex.name[-4:] == ".tex" :

        st.success("Fichier bien reçu !")
        return fichierTex
    else :
        if fichierTex is not None :
            st.error("Erreur, cela ne semble pas être un fichier tex. Chargez un autre fichier SVP")
        return None

def recupNom():
    titre = st.text_input(" Nom du fichier : ", value="EvalALaCarte", key = 1, max_chars = 30, help="Personnalisez le nom du fichier.",)
    return titre

def interfaceGraphique1():
    with st.expander("1- Entrer ici le titre de l'évaluation. ") :
        titre = recupTitre()
        if titre != "":
            st.markdown(":green[_Titre de l'évaluation enregistré :_] "+titre)

    with st.expander("2- Choisir la classe évaluée. ") :
        col1, col2 = st.columns(2)
        with col1:
            niveau = choixNiveau()
        with col2:
            classe =  choixClasse()
        
        classe = niveau + classe
        st.write(':green[_Nom de la classe enregistré :_] ', classe)

    with st.expander("3- Entrer ici la date de l'évaluation.") :
        date = choixDate()
        if date != "":
            st.markdown(":green[_Date de l'évaluation enregistrée :_ ] "+date.strftime("%d/%m/%Y"))
        
    with st.expander("4- Entrer ici le nom de l'établissement.") :
        etab = recupEtab()
        if etab != "":
            st.markdown(":green[_Nom de l'établissement enregistré :_ ]"+etab)
    
    with st.expander("5- Entrer ici le nom (sans l'extension) du fichier .tex qui sera créé.") :
        nom_fichier_eval = recupNom()+".tex"
        if nom_fichier_eval != "":
            st.markdown(":green[_Nom du fichier créé :_] "+nom_fichier_eval)
        
    return (etab, titre, date.strftime("%d/%m/%Y"), classe, nom_fichier_eval)


def interfaceGraphique2():
    
    n=1
    devoircommun ="Non"
    st.write(str(n)," - Voulez-vous ajouter un ou des exercices communs à tous les élèves ?")
    exosCommuns = st.radio('VOTRE REPONSE', ('Non', 'Oui'), horizontal = True, key= "tic")
    if exosCommuns == "Oui":
        n+=1
        st.markdown(''':green[Dans l'onglet "Import", n'oubliez pas d'ajouter un fichier .tex contenant le ou les exercice(s) commun(s).]''')
        st.write(str(n)," - Voulez-vous aussi un sujet ne contenant que les exercices communs ?")
        devoircommun = st.radio('VOTRE REPONSE', ('Non', 'Oui'), horizontal = True, key = "tac")
        if devoircommun == "Oui":
            st.markdown(''':green[Dans l'onglet "Export", n'oubliez pas de télécharger le fichier sujetcommun.tex.]''')
    n+=1
    st.write(str(n)," - Voulez-vous ajouter un exercice facultatif à tous les élèves ?")
    
    exoFacultatif = st.radio('VOTRE REPONSE', ('Non', 'Oui'), horizontal = True, key= "toc")
    if exoFacultatif == "Oui":
        st.markdown(''':green[Dans l'onglet "Import", n'oubliez pas d'ajouter un fichier .tex contenant l'exercice facultatif.]''')
    
    return (exosCommuns, exoFacultatif, devoircommun)