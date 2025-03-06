#!/usr/bin/env python3
"""
Script pour copier les fichiers JSON vers le dossier output.
Usage: python copy_json_to_output.py chemin_source [dossier_destination]
"""

import os
import sys
import shutil
import glob
import time

def copy_json_files(source_path, destination="output"):
    """
    Copie tous les fichiers JSON depuis source_path vers le dossier destination.
    
    Args:
        source_path (str): Chemin source pour chercher les fichiers JSON
        destination (str): Dossier de destination (par défaut: "output")
    
    Returns:
        tuple: (nombre de fichiers copiés, liste des fichiers copiés)
    """
    # Créer le dossier de destination s'il n'existe pas
    if not os.path.exists(destination):
        print(f"Create folder {destination}")
        os.makedirs(destination)
    
    # Trouver tous les fichiers JSON récursivement
    json_pattern = os.path.join(source_path, "**", "*.json")
    json_files = glob.glob(json_pattern, recursive=True)
    
    if not json_files:
        print(f"No JSON File found {source_path}")
        return 0, []
    
    # Copier chaque fichier JSON
    copied_files = []
    copied_count = 0
    
    for json_file in json_files:
        filename = os.path.basename(json_file)
        destination_path = os.path.join(destination, filename)
        
        # Vérifier si le fichier existe déjà
        if os.path.exists(destination_path):
            source_mtime = os.path.getmtime(json_file)
            dest_mtime = os.path.getmtime(destination_path)
            
            # Si le fichier source est plus récent, on le remplace
            if source_mtime > dest_mtime:
                print(f"Update {filename}")
                shutil.copy2(json_file, destination_path)
                copied_files.append(destination_path)
                copied_count += 1
        else:
            print(f"Copy {filename}")
            shutil.copy2(json_file, destination_path)
            copied_files.append(destination_path)
            copied_count += 1
    
    return copied_count, copied_files

def main():
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) < 2:
        print("Usage: python copy_json_to_output.py chemin_source [dossier_destination]")
        print("Example: python copy_json_to_output.py ./data output")
        sys.exit(1)
    
    source_path = sys.argv[1]
    
    # Vérifier si le chemin source existe
    if not os.path.exists(source_path):
        print(f"root path {source_path} n'existe pas.")
        sys.exit(1)
    
    # Destination par défaut ou fournie en argument
    destination = "output"
    if len(sys.argv) > 2:
        destination = sys.argv[2]
    
    print(f"Search JSON in {source_path}")
    start_time = time.time()
    
    count, files = copy_json_files(source_path, destination)
    
    elapsed_time = time.time() - start_time
    
    print(f"\n Finish {elapsed_time:.2f} secondes!")
    print(f"📊 {count} files JSON move to {destination}")
    
    if count > 0:
        print("\nFichiers moved:")
        for i, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            print(f"  {i}. {filename}")

if __name__ == "__main__":
    main()
