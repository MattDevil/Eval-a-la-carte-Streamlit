import os, os.path, random, glob, csv, subprocess
import streamlit as st
import numpy as np
import pandas as pd

import modules.Définition as defi
import modules.divers as divers
from PIL import Image


######################################
#  Config générale de l'appli
######################################

st.set_page_config(
   page_title="Eval à la carte",
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
        st.markdown('''
        Version : 0.3 du 01-01-2023

        Auteur : Matthieu DEVILLERS matthieu.devillers@ac-rennes.fr

        Licence : [CC-BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)
        
        Une partie du code provient d'un [script python](http://revue.sesamath.net/spip.php?article535) écrit par Rémi Angot et mis à disposition sous licence A-GPL
        
         
        ''')
        
    with st.expander("Documentation"):
        st.markdown(""" Pour installer et utiliser cette application en local, il vous faudra :""")
        st.markdown("""                    
        ##### 1. Cloner le dépot ou télécharger l'ensemble des fichiers. 
        
        ##### 2. Installer streamlit sur votre machine en suivant cette [Documentation](https://docs.streamlit.io/library/get-started/installation)
        
        ##### 3. Lancer l'application localement
        
        """)
        
        st.markdown("""
        ```bash
        
        cd EVAL_A_La_Carte
        
        pipenv shell
        
        streamlit run Accueil.py
        ```        
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


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Accueil","Paramètres", "Options", "Bilan", "Import", "Export"])

with tab1:
    
    st.write("""


    Paramétrez l'évaluation dans *Paramètres* et choisissez ensuite les *options*.
    
    Vérifiez vos choix dans *Bilan*.

    Ajoutez les demandes des élèves dans *Import*.

    Générez et téléchargez l'évaluation au format .tex dans *Export*.

    """)

    

with tab2:
    
    informations = defi.interfaceGraphique1()
    
    

with tab3:
    
    informations2 = defi.interfaceGraphique2()
    

with tab4:
    st.write('''
    ##### Les paramétres suivants seront utilisés :

    ''')

    col10, col20 = st.columns(2, gap="medium")

    with col10:
        infos = ["Nom de l'établissement","Titre de l'évaluation","Date de l'évaluation","Classe ou groupe évalué","Nom du fichier .tex créé"]
        for i in range(5):
            st.write(infos[i]," : ",informations[i])  

    with col20:
        infos2 = ["Présence d'exercice(s) commun(s)", "Présence d'un exercice facultatif", "Que les exercices communs"]
        for i in range(3):
            st.write(infos2[i]," : ",informations2[i])



with tab5:
    compteur = 1
    st.markdown(str(compteur)+". Glissez-déposez ici le fichier csv des demandes des élèves (export SACoche) : ") 
    demandes = defi.recupDemandes()
    
    if informations2[0] == "Oui" :
        compteur +=1
        st.markdown(str(compteur)+". Glissez-déposez ici le fichier .tex des exercices communs : ")
        communs = defi.recupTex(1)
        if communs is not None:
            with open(os.path.join(communs.name),"wb") as f:
                f.write(communs.getbuffer())
        
        compteur +=1
        st.markdown(str(compteur)+". Glissez-déposez ici le fichier .tex des compétences des exercices communs : ")
        compeCommuns = defi.recupTex(2)
        if compeCommuns is not None:
            with open(os.path.join(compeCommuns.name),"wb") as f:
                f.write(compeCommuns.getbuffer())
         
    if informations2[1] == "Oui" :
        
        compteur +=1
        st.markdown(str(compteur)+". Glissez-déposez ici le fichier .tex de l'exercice facultatif : ")

        facultatif = defi.recupTex(3)
        if facultatif is not None:
            with open(os.path.join(facultatif.name),"wb") as f:
                f.write(facultatif.getbuffer())
        
        compteur +=1
        st.markdown(str(compteur)+". Glissez-déposez ici le fichier .tex des compétences de l'exercice facultatif : ")
        compeFacultatif = defi.recupTex(4)
        if compeFacultatif is not None:
            with open(os.path.join(compeFacultatif.name),"wb") as f:
                f.write(compeFacultatif.getbuffer())
 
with tab6:
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
        nom_fichier_eval= informations[4]
        devoirclasse= informations2[2]
        exofacultatif=informations2[1]
 
    
        # Création du fichier nom_fichier_eval.tex

        fichier_eval = open(nom_fichier_eval, "a", encoding='UTF-8')

        #--------------------
        # Ajout du Préambule à nom_fichier_eval.tex
        #--------------------

        nom_fichier_preambule="en-tete_fichier.tex"
        fichier_preambule=open(nom_fichier_preambule, "r", encoding='UTF-8')
        texte_preambule=fichier_preambule.read()
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
            if len(demandes_eleve) !=0 :
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
                
                if informations2[0] == "o" :
                    print("\\input{tableau-items-communs.tex} ",file=fichier_eval)
                


        #--------------------
        # Ajout du tableau avec les compétences à la carte.
        #--------------------

                for i in range(1,len(demandes_eleve)) :
                    nom_item=liste_noms_items[k][i]
                    print("* ",nom_item," & & & & & \\\ ",file=fichier_eval)
                    print("\\hline",file=fichier_eval)
                
                if informations2[1]=="o" :
                    print("\\input{tableau-facultatif.tex} \\",file=fichier_eval)
              
                print("\end{tabular}",file=fichier_eval)
                print("\end{center}",file=fichier_eval)
                print("\end{footnotesize}",file=fichier_eval)
        #--------------------
        # Ajout des exercices communs à la classe.
        #--------------------
                if informations2[0] == "o" :
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

                
                if informations2[1]=="o" :
                    print("\\input{facultatif.tex} \\",file=fichier_eval)                        

                                             
        print("\\end{document}",file=fichier_eval)

        fichier_eval.close()
        
        if st.button("Compiler avec pdfLatex"):
            os.system("pdflatex "+nom_fichier_eval)
            #os.startfile(nom_fichier_eval+".pdf")
            subprocess.call(['pdflatex',nom_fichier_eval])
            nom_fichier_pdf = nom_fichier_eval[:-3]+"pdf"
            st.write(nom_fichier_pdf)
            with open(nom_fichier_eval, 'rb') as f:
                if st.download_button('Téléchargez le fichier .tex', f, file_name=nom_fichier_eval):
                    f.close()
                    if st.button("Effacer le fichier .tex"):
                        os.system("rm "+nom_fichier_eval)
                        #os.startfile(nom_fichier_eval+".pdf")
                        subprocess.call(['rm',nom_fichier_eval])
                        st.write("Done")