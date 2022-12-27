import os, os.path, random, glob, csv, subprocess
import streamlit as st
import numpy as np
import pandas as pd

import modules.Définition as defi
import modules.divers as divers
from PIL import Image

st.set_page_config(
   page_title="A_la_carte",
   page_icon=":boat:",
   layout="wide",
   initial_sidebar_state="expanded",
)


######################################
#   Barre latérale
######################################

with st.sidebar :
    

    image = Image.open('img/logo.png')

    st.image(image)
    
    with st.expander("Licence / crédits"):
        st.write("""
        Version : 0.2 du 26-12-2022

        Auteur : Matthieu DEVILLERS matthieu.devillers@ac-rennes.fr

        Licence : [CC-BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)
        """)
        
    with st.expander("Documentation"):
        st.write("""
            
        à compléter...

        """)

######################################
#   Page principale
######################################
demandes = []

st.write("""
## Evaluation à la carte

""")



#####################################
#   Pages intérieures
#####################################


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Accueil","Paramètres", "Bilan", "Import", "Export"])

with tab1:
    
    st.write("""


    Paramétrez l'évaluation dans *Paramètres*.
    
    Vérifiez vos choix dans *"Bilan"*.

    Ajoutez les demandes des élèves dans *"Import"*.

    Générez et téléchargez l'évaluation dans *"Export"*.

    """)

    

with tab2:
    
    informations = defi.interfaceGraphique1()
    
    informations2 = defi.interfaceGraphique2()



with tab3:
    st.write('''
    ##### Les paramétres suivants seront utilisés :

    ''')

    col10, col20 = st.columns(2, gap="medium")

    with col10:
        infos = ["Nom de l'établissement","Titre de l'évaluation","Date de l'évaluation","Classe ou groupe évalué"]
        for i in range(4):
            st.write(infos[i]," : ",informations[i])  

    with col20:
        infos2 = ["Nom du fichier .tex","Présence d'exercice(s) commun(s)", "Présence d'un exercice facultatif", "Que les exercices communs"]
        for i in range(4):
            st.write(infos2[i]," : ",informations2[i])



with tab4:
    compteur = 1
    
    html_str = f"""
    <h5>{compteur}. Glissez-déposez ici le fichier csv des demandes des élèves (export SACoche) : </h5>
    """
    st.markdown(html_str, unsafe_allow_html=True)
     
    demandes = defi.recupDemandes()
    
    if informations2[1] == "o" :
        compteur +=1
        html_str2 = f"""
        <h5>{compteur}. Glissez-déposez ici le fichier tex des exercices communs : </h5>
        """
        st.markdown(html_str2, unsafe_allow_html=True)

        communs = defi.recupTex(1)
        
        compteur +=1
        html_str3 = f"""
        <h5>{compteur}. Glissez-déposez ici le fichier tex des compétences des exercices communs : </h5>
        """
        st.markdown(html_str3, unsafe_allow_html=True)

        compeCommuns = defi.recupTex(2)
        
        
    if informations2[2] == "o" :
        
        compteur +=1
        html_str4 = f"""
        <h5>{compteur}. Glissez-déposez ici le fichier tex de l'exercice facultatif : </h5>
        """
        st.markdown(html_str4, unsafe_allow_html=True)

        facultatif = defi.recupTex(3)
        
        
        compteur +=1
        html_str5 = f"""
        <h5>{compteur}. Glissez-déposez ici le fichier tex des compétences de l'exercice facultatif : </h5>
        """
        st.markdown(html_str5, unsafe_allow_html=True)

        facultatif = defi.recupTex(4)
   
with tab5:
    if st.button("Générer l'évaluation"):
        liste_noms_items=[]
        date = informations[2]
        if os.name=="posix" :
            sep="/"
        else :
            sep="\\"
        repertoire_courant=os.getcwd()
        repertoire_items='items'
        classe= informations[3]
        titreeval= informations[1]
        nom_fichier_eval= informations2[0]
        devoirclasse= informations2[3]
        exofacultatif=informations2[2]
 
#         Tab1=("date", "repertoire_items", "classe", "titreeval", "nom_fichier_eval","devoirclasse", "exofacultatif", "sep")
#         Tab2=(date, repertoire_items, classe, titreeval, nom_fichier_eval,devoirclasse, exofacultatif, sep)
#         for i in range (8) :
#             st.write(Tab1[i]," = ", Tab2[i])
          
        # Création du fichier nom_fichier_eval.tex

        fichier_eval = open(nom_fichier_eval, "a", encoding='UTF-8')

        #--------------------
        # Ajout du Préambule à nom_fichier_eval.tex
        #--------------------

        nom_fichier_preambule="en-tete_fichier.tex"
        fichier_preambule=open(nom_fichier_preambule, "r", encoding='UTF-8')
        texte_preambule=fichier_preambule.read()
        st.write(texte_preambule)
        fichier_preambule.close()
        print(texte_preambule,file=fichier_eval)
        
        #--------------------
        # Ajout de l'en-tête en_tete_eleve.tex
        #--------------------
        nom_fichier_en_tete="en-tete_eleve"
        fichier_en_tete=open(nom_fichier_en_tete+".tex", "r", encoding='UTF-8')
        texte_en_tete=fichier_en_tete.read()
        fichier_en_tete.close()

        # Ajout de \begin{document}

        print("\\begin{document}",file=fichier_eval)


        #--------------------
        # Choix des items
        #--------------------
        #os.makedirs('temp', exist_ok=True)
        demandes.to_csv('Listedemandes.csv')
                
        liste_demandes,liste_noms_items=divers.analyse_demandes("Listedemandes.csv",liste_noms_items)
        
        k=0

        for demandes_eleve in liste_demandes :
            titre="Pour "+demandes_eleve[0]
            print(titre.center(50,'-'))
            if len(demandes_eleve)==0 :
                print("Aucune demande")
            else :
                texte_en_tete_perso=texte_en_tete
                texte_en_tete_perso=texte_en_tete_perso.replace("@NOM@",demandes_eleve[0])
                texte_en_tete_perso=texte_en_tete_perso.replace("@date@",date) # Ajout de la date du devoir dans l'entête
                texte_en_tete_perso=texte_en_tete_perso.replace("@classe@",classe) # Ajout du nom de la classe ou du niveau dans l'entête
                texte_en_tete_perso=texte_en_tete_perso.replace("@titreeval@",titreeval) # Ajout du titre 
                print(texte_en_tete_perso,file=fichier_eval)
            
        #--------------------
        # Ajout du tableau avec les compétences de la classe.
        #--------------------
                print("\\input{tableau-item-classe.tex} ",file=fichier_eval)
                


        #--------------------
        # Ajout du tableau avec les compétences à la carte.
        #--------------------

                for i in range(1,len(demandes_eleve)) :
                    nom_item=liste_noms_items[k][i]
                    print("* ",nom_item," & & & & \\\ ",file=fichier_eval)
                    print("\\hline",file=fichier_eval)
              
                print("\end{tabular}",file=fichier_eval)
                print("\end{center}",file=fichier_eval)
                print("\end{footnotesize}",file=fichier_eval)
        #--------------------
        # Ajout des exercices communs à la classe.
        #--------------------
                # if exocommuns :
                print("\\input{exercices-communs.tex} \\",file=fichier_eval)
                
                

        #--------------------
        # Ajout des exercices à la carte.
        #--------------------        

                chemin_item = []
                
                for i in range(1,len(demandes_eleve)) :
                    id_item=demandes_eleve[i]
                    if divers.tex_existe(id_item, repertoire_items, sep) :
                        chemin_item=divers.tex_hasard_item(id_item, repertoire_items,sep)
                        print("\\input{"+chemin_item+"} \\par ",file=fichier_eval)
                        print("\\medskip",file=fichier_eval)
                k=k+1

        #--------------------
        # Ajout de l'exercice facultatif et fin du document.
        #--------------------        

                
                if (exofacultatif=="O") or (exofacultatif=="o") :
                    print("\\input{facultatif.tex} \\",file=fichier_eval)                        

                                             
        print("\\end{document}",file=fichier_eval)

        fichier_eval.close()

        


