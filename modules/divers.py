
import os, os.path, random, glob, csv, subprocess
import streamlit as st

#Cherche si un fichier .tex commençant par id_item existe dans repertoire_items
def tex_existe(id_item, repertoire_items, sep):
    liste_fichiers_tex=glob.glob(repertoire_items+sep+id_item+"_*.tex")
    if not liste_fichiers_tex :
        st.write("Pas d'exercice pour "+id_item)
        return None
    else :
        return liste_fichiers_tex

#Ne garde que la 1ère partie de l'identifiant d'un item (avant l'espace)        
def id_item(reference) :
    return reference.partition(" ")[0]

#Ne garde que le nom de l'item (après les espaces, le statut et le coefficient)
def nom_item(reference) :
    return reference.partition(" ")[2].partition(" ")[2].partition(" ")[2]

#Choisit un fichier .tex au hasard pour un item donné
def tex_hasard_item(id_item, repertoire_items, sep) :
    liste_fichiers_tex=glob.glob(repertoire_items+sep+id_item+'_*.tex')
    tex=random.choice(liste_fichiers_tex)
    #print("Fichier choisi :",tex)
    return tex

#Transforme le fichier csv de SACoche en tableau
#[['Nom1','item1','item2],[['Nom2','item1']]
def analyse_demandes(fichier_csv_sacoche, liste_noms_items) :
    tableau=[]
    liste_noms=[]
    liste_demandes=[]
    
    fichier_demandes=open(fichier_csv_sacoche,"r",encoding="UTF-8")
    lecture=csv.reader(fichier_demandes,delimiter=",")

    for ligne in lecture :
        tableau.append(ligne)

    fichier_demandes.close()
    
    nbr_colonnes=len(tableau[1])
    nbr_lignes=len(tableau)
    ligne_noms=nbr_lignes-7
    colonne_items=nbr_colonnes-1
    for eleve in range(2,colonne_items) :
        liste_demandes_temp=[]
        liste_noms_items_temp=[] # liste temporaire
        liste_demandes_temp.append(tableau[ligne_noms][eleve])
        liste_noms_items_temp.append(tableau[ligne_noms][eleve])
        for i in range (1,ligne_noms) :
            if tableau[i][eleve]=="P" :
                liste_demandes_temp.append(id_item(tableau[i][colonne_items]))
                liste_noms_items_temp.append(nom_item(tableau[i][colonne_items])) # récupération noms complets des items du csv
        liste_demandes.append(liste_demandes_temp)
        liste_noms_items.append(liste_noms_items_temp)
    return (liste_demandes, liste_noms_items)
