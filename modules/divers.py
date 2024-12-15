
import os, os.path, random, glob, csv, subprocess
import streamlit as st
import shutil

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

## Ajout Claude
def list_files_and_folders(directory):
    """Liste récursivement tous les fichiers et dossiers."""
    items = []
    for root, dirs, files in os.walk(directory):
        # Calculer le chemin relatif depuis le répertoire de base
        rel_path = os.path.relpath(root, directory)
        
        # Ajouter les dossiers
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            rel_full_path = os.path.join(rel_path, dir_name) if rel_path != '.' else dir_name
            items.append({
                'type': 'folder', 
                'path': rel_full_path, 
                'full_path': full_path
            })
        
        # Ajouter les fichiers
        for file_name in files:
            full_path = os.path.join(root, file_name)
            rel_full_path = os.path.join(rel_path, file_name) if rel_path != '.' else file_name
            items.append({
                'type': 'file', 
                'path': rel_full_path, 
                'full_path': full_path
            })
    
    return sorted(items, key=lambda x: x['path'])

def file_management_tab(items_directory):
    """Onglet de gestion des fichiers et dossiers."""
    st.header("Gestion des fichiers et dossiers")
    
    # Section de création de sous-dossiers
    st.subheader("Créer un nouveau dossier")
    new_folder_name = st.text_input("Nom du nouveau dossier")
    new_folder_parent = st.selectbox("Dossier parent", 
        ['.'] + [item['path'] for item in list_files_and_folders(items_directory) if item['type'] == 'folder']
    )
    
    if st.button("Créer le dossier"):
        if new_folder_name:
            try:
                new_folder_path = os.path.join(items_directory, new_folder_parent, new_folder_name)
                os.makedirs(new_folder_path, exist_ok=True)
                st.success(f"Dossier {new_folder_name} créé avec succès dans {new_folder_parent}")
            except Exception as e:
                st.error(f"Erreur lors de la création du dossier : {e}")
    
    # Section de suppression de dossiers
    st.subheader("Supprimer un dossier")
    folders_to_delete = [item['path'] for item in list_files_and_folders(items_directory) if item['type'] == 'folder']
    folder_to_delete = st.selectbox("Sélectionner le dossier à supprimer", folders_to_delete)
    
    if st.button("Supprimer le dossier"):
        try:
            full_path = os.path.join(items_directory, folder_to_delete)
            shutil.rmtree(full_path)
            st.success(f"Dossier {folder_to_delete} supprimé avec succès")
        except Exception as e:
            st.error(f"Erreur lors de la suppression du dossier : {e}")
    
    # Section de téléchargement de fichiers
    st.subheader("Télécharger des fichiers")
    uploaded_files = st.file_uploader(
        "Choisissez les fichiers à télécharger", 
        accept_multiple_files=True
    )
    
    upload_location = st.selectbox("Emplacement de téléchargement", 
        ['.'] + [item['path'] for item in list_files_and_folders(items_directory) if item['type'] == 'folder']
    )
    
    if uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(items_directory, upload_location, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success(f"{len(uploaded_files)} fichiers téléchargés avec succès")
        except Exception as e:
            st.error(f"Erreur lors du téléchargement : {e}")
    
    # Section de suppression de fichiers
    st.subheader("Supprimer des fichiers")
    all_files = [item['path'] for item in list_files_and_folders(items_directory) if item['type'] == 'file']
    files_to_delete = st.multiselect("Sélectionner les fichiers à supprimer", all_files)
    
    if st.button("Supprimer les fichiers sélectionnés"):
        try:
            for file in files_to_delete:
                os.remove(os.path.join(items_directory, file))
            st.success(f"{len(files_to_delete)} fichiers supprimés avec succès")
        except Exception as e:
            st.error(f"Erreur lors de la suppression : {e}")
    
    # Section de renommage de fichiers
    st.subheader("Renommer un fichier")
    file_to_rename = st.selectbox("Sélectionner le fichier à renommer", all_files)
    new_filename = st.text_input("Nouveau nom de fichier")
    
    if st.button("Renommer le fichier"):
        if new_filename:
            try:
                old_path = os.path.join(items_directory, file_to_rename)
                new_path = os.path.join(os.path.dirname(old_path), new_filename)
                os.rename(old_path, new_path)
                st.success(f"Fichier renommé de {file_to_rename} à {new_filename}")
            except Exception as e:
                st.error(f"Erreur lors du renommage : {e}")
    
    # Section de déplacement de fichiers
    st.subheader("Déplacer des fichiers")
    files_to_move = st.multiselect("Sélectionner les fichiers à déplacer", all_files)
    destination_folder = st.selectbox("Dossier de destination", 
        ['.'] + [item['path'] for item in list_files_and_folders(items_directory) if item['type'] == 'folder']
    )
    
    if st.button("Déplacer les fichiers"):
        try:
            for file in files_to_move:
                src_path = os.path.join(items_directory, file)
                dst_path = os.path.join(items_directory, destination_folder, os.path.basename(file))
                shutil.move(src_path, dst_path)
            st.success(f"{len(files_to_move)} fichiers déplacés avec succès")
        except Exception as e:
            st.error(f"Erreur lors du déplacement : {e}")
    
    # Affichage de l'arborescence actuelle
    st.subheader("Arborescence actuelle")
    current_items = list_files_and_folders(items_directory)
    
    # Création d'un dictionnaire pour la représentation hiérarchique
    tree_view = {}
    for item in current_items:
        parts = item['path'].split(os.path.sep)
        current_level = tree_view
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = item['type']
    
    def display_tree(tree, indent=''):
        for name, content in tree.items():
            if isinstance(content, dict):
                st.text(f"{indent}📁 {name}")
                display_tree(content, indent + '  ')
            else:
                icon = '📄' if content == 'file' else '📁'
                st.text(f"{indent}{icon} {name}")
    
    display_tree(tree_view)
