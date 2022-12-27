#Rémi ANGOT CC-By-SA (modifié par Matthieu DEVILLERS)
#Les fichiers exercice .tex sont dans /items et sont nommés id_textelibre.tex 
#Le fichier exercices-communs.tex contient les exercices communs à toute la classe.
#Le fichier facultatif.tex contient un exercice facultatif placé en fin d'éval (fichier vide au besoin). 
#Le fichier tableau-item-classe contient le cartouche SACoche avec la liste des items évalués dans les exercices communs.
#Le fichier csv est obtenu avec SACoche (saisie déportée avec scores, d'une évaluation créée suite à des demandes d'élèves).


import os, os.path, random, glob, csv, subprocess


#Cherche si un fichier .tex commençant par id_item existe dans repertoire_items
def tex_existe(id_item):
    liste_fichiers_tex=glob.glob(repertoire_items+sep+id_item+'_*.tex')
    if not liste_fichiers_tex :
        print("Pas d'exercice pour "+id_item)
    else :
        return True

#Ne garde que la 1ère partie de l'identifiant d'un item (avant l'espace)        
def id_item(reference) :
    return reference.partition(" ")[0]

#Ne garde que le nom de l'item (après les espaces, le statut et le coefficient)
def nom_item(reference) :
    return reference.partition(" ")[2].partition(" ")[2].partition(" ")[2]

#Choisit un fichier .tex au hasard pour un item donné
def tex_hasard_item(id_item) :
    liste_fichiers_tex=glob.glob(repertoire_items+'/'+id_item+'_*.tex')
    tex=random.choice(liste_fichiers_tex)
    #print("Fichier choisi :",tex)
    return tex

#Transforme le fichier csv de SACoche en tableau
#[['Nom1','item1','item2],[['Nom2','item1']]
def analyse_demandes(fichier_csv_sacoche) :
    tableau=[]
    liste_noms=[]
    liste_demandes=[]
    

    fichier_demandes=open(fichier_csv_sacoche,"r",encoding="iso-8859-15")
    lecture=csv.reader(fichier_demandes,delimiter=";",)

    for ligne in lecture :
        tableau.append(ligne)

    fichier_demandes.close()
    
    nbr_colonnes=len(tableau[1])
    nbr_lignes=len(tableau)
    ligne_noms=nbr_lignes-7
    colonne_items=nbr_colonnes-1
    date.append(tableau[nbr_lignes-4]) # récupération de la date du devoir indiquée dans le csv 
    for eleve in range(1,colonne_items) :
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
    print(liste_demandes, " \n")
    print (liste_noms_items)
    return liste_demandes

######################################################
# Recherche de la liste des items
######################################################


#--------------------
# Début
#--------------------
liste_noms_items=[]
date=[]
if os.name=="posix" :
    sep="/"
else :
    sep="\\"
repertoire_courant=os.getcwd()
repertoire_items='items'
titre=""
print(titre.center(50,'-'))
titre="Evaluation à la carte (v. 2018-11-14)"
print(titre.center(50,'-'))
titre=""
print(titre.center(50,'-'))
classe=input("Quel est le nom (ou le niveau) de la classe (ou du groupe) évalué ?")
titreeval=input("Quel est le titre de l'évaluation ?")
nom_fichier_demandes=input("Nom du fichier récupéré depuis SACoche (sans extension) :")
while not (os.path.exists(nom_fichier_demandes+".csv")) :
    print("Ce fichier n'existe pas !")
    nom_fichier_demandes=input("Nom du fichier (sans extension) :")

print("Création d'un fichier LaTeX pour l'évaluation.")
nom_fichier_eval=input("Nom du fichier (sans extension) :")
while os.path.exists(nom_fichier_eval+'.tex') :
    print("Ce fichier existe déjà, donnez le nom d'un nouveau fichier.")
    nom_fichier_eval=input("Nom du fichier (sans extension) :")

devoirclasse=input("Voulez-vous créer un sujet ne contenant que les exercices communs ? (o|n) :")
exofacultatif=input("Voulez-vous ajouter un exercice facultatif à la fin du sujet ? (o|n) :")

# Création du fichier nom_fichier_eval.tex

fichier_eval = open(nom_fichier_eval+'.tex', "a", encoding='UTF-8')

#--------------------
# Ajout du Préambule à nom_fichier_eval.tex
#--------------------

nom_fichier_preambule="en-tete_fichier"
fichier_preambule=open(nom_fichier_preambule+".tex", "r", encoding='UTF-8')
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

liste_demandes=analyse_demandes(nom_fichier_demandes+".csv")

k=0

for demandes_eleve in liste_demandes :
    titre="Pour "+demandes_eleve[0]
    print(titre.center(50,'-'))
    if len(demandes_eleve)==0 :
        print("Aucune demande")
    else :
        texte_en_tete_perso=texte_en_tete
        texte_en_tete_perso=texte_en_tete_perso.replace("@NOM@",demandes_eleve[0])
        texte_en_tete_perso=texte_en_tete_perso.replace("@date@",date[0][0]) # Ajout de la date du devoir dans l'entête
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

        print("\\input{exercices-communs.tex} \\",file=fichier_eval)
        
        

#--------------------
# Ajout des exercices à la carte.
#--------------------        


        
        for i in range(1,len(demandes_eleve)) :
            id_item=demandes_eleve[i]
            if tex_existe(id_item) :
                chemin_item=tex_hasard_item(id_item)
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

#--------------------
# Compilation
#--------------------
titre=""
print(titre.center(50,'-'))
titre="Le fichier LaTeX est maintenant prêt"
print(titre.center(50,'-'))
compil=input("Souhaitez-vous compiler le fichier avec pdfLaTeX ? (O|N)")
if compil in ["","O","o","oui","OUI"] :
    os.system("pdflatex "+nom_fichier_eval+".tex")
    #os.startfile(nom_fichier_eval+".pdf")
    subprocess.call(['pdflatex',nom_fichier_eval+".tex"])


if (devoirclasse in["o", "O","oui","OUI"]):
    
#--------------------
# Ajout d'un sujet ne contenant que les exercices communs pour les élèves n'ayant pas fait de demande SACoche
#--------------------

    nom_fichier_eval=nom_fichier_eval+"-commun"
    fichier_eval = open(nom_fichier_eval+'.tex', "a", encoding='UTF-8')

#--------------------
# Ajout du Préambule à nom_fichier_eval.tex
#--------------------

    nom_fichier_preambule="en-tete_fichier"
    fichier_preambule=open(nom_fichier_preambule+".tex", "r", encoding='UTF-8')
    texte_preambule=fichier_preambule.read()
    fichier_preambule.close()
    print(texte_preambule,file=fichier_eval)


#--------------------
# Ajout de l'en-tête en_tete_eleve_commun.tex
#--------------------


    nom_fichier_en_tete="en-tete_eleve"
    fichier_en_tete=open(nom_fichier_en_tete+".tex", "r", encoding='UTF-8')
    texte_en_tete=fichier_en_tete.read()
    fichier_en_tete.close()

# Ajout de \begin{document}

    print("\\begin{document}",file=fichier_eval)

    texte_en_tete_perso=texte_en_tete
    texte_en_tete_perso=texte_en_tete_perso.replace("@NOM@","Nom : ............................................   Prénom : ............................................")
    texte_en_tete_perso=texte_en_tete_perso.replace("@date@",date[0][0]) # Ajout de la date du devoir dans l'entête
    texte_en_tete_perso=texte_en_tete_perso.replace("@classe@",classe) # Ajout du nom de la classe ou du niveau dans l'entête
    texte_en_tete_perso=texte_en_tete_perso.replace("@titreeval@",titreeval) # Ajout du titre 
    print(texte_en_tete_perso,file=fichier_eval)

#--------------------
# Ajout du tableau avec les compétences de la classe.
#--------------------
    tableau_item_classe="tableau-item-classe"
    texte_tableau_item_classe=open(tableau_item_classe+".tex","r", encoding='UTF-8')
    tableau_it=texte_tableau_item_classe.read()
    texte_tableau_item_classe.close()
    
    print(tableau_it,file=fichier_eval)
    print("\end{tabular}",file=fichier_eval)
    print("\end{center}",file=fichier_eval)
    print("\end{footnotesize}",file=fichier_eval)
#--------------------
# Ajout des exercices communs à la classe et exercice facultatif
#--------------------

    print("\\input{exercices-communs.tex} \\",file=fichier_eval)

    if (exofacultatif=="O") or (exofacultatif=="o") :
        print("\\input{facultatif.tex} \\",file=fichier_eval)                        


                                     
    print("\\end{document}",file=fichier_eval)

    fichier_eval.close()

#--------------------
# Compilation
#--------------------
    titre=""
    print(titre.center(50,'-'))
    titre="Le fichier LaTeX est maintenant prêt"
    print(titre.center(50,'-'))
    compil=input("Souhaitez-vous compiler le fichier avec pdfLaTeX ? (O|N)")
    if compil in ["","O","o","oui","OUI"] :
        os.system("pdflatex "+nom_fichier_eval+".tex")
        #os.startfile(nom_fichier_eval+".pdf")
        subprocess.call(['pdflatex',nom_fichier_eval+".tex"])
