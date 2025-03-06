from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import sys
import subprocess


#### ADD and change
## Docker 
## Doc git ... 
## Push public ..

app = Flask(__name__, static_folder='static')
CORS(app)

# Répertoire de sortie pour les résultats
OUTPUT_DIR = "output"

# Dictionnaire des scripts disponibles dans le dossier lib
SCRIPTS = {
    "1": "lib/search_duck.py",
    "4": "lib/llm_duck.py",
    "5": "lib/llm_duck_image.py",
    "6": "lib/llm_duck_videos.py",
    "7": "lib/llm_duck_wikipedia.py",
    "8": "lib/llm_duck_articles.py",
    "9": "lib/llm_duck_company.py",
    "10": "lib/llm_duck_news.py",
}

# Route pour la page principale
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Récupérer la liste des scripts disponibles
@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    script_list = []
    for key, path in SCRIPTS.items():
        name = path.split('/')[-1].replace('.py', '').replace('_', ' ').title()
        script_list.append({"id": key, "name": name, "path": path})
    return jsonify(script_list)

# Lire le fichier de requêtes
@app.route('/api/queries', methods=['GET'])
def get_queries():
    try:
        with open("inputs.txt", "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f.readlines() if line.strip()]
        return jsonify(queries)
    except FileNotFoundError:
        # Crée un fichier vide s'il n'existe pas
        with open("inputs.txt", "w", encoding="utf-8") as f:
            pass
        return jsonify([])

# Sauvegarder les requêtes dans le fichier
@app.route('/api/queries', methods=['POST'])
def save_queries():
    data = request.json
    if 'queries' in data:
        try:
            with open("inputs.txt", "w", encoding="utf-8") as f:
                for query in data['queries']:
                    f.write(f"{query}\n")
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    return jsonify({"success": False, "error": "Données manquantes"})

# Exécuter un script
@app.route('/api/execute', methods=['POST'])
def execute_script():
    data = request.json
    results = []
    
    # Vérifier les paramètres
    if 'script_id' not in data:
        return jsonify({"success": False, "error": "ID de script manquant"})
    
    script_id = data['script_id']
    
    if script_id not in SCRIPTS:
        return jsonify({"success": False, "error": "Script invalide"})
    
    # Récupérer les requêtes
    if 'use_file' in data and data['use_file']:
        try:
            with open("inputs.txt", "r", encoding="utf-8") as f:
                queries = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return jsonify({"success": False, "error": "Fichier inputs.txt introuvable"})
    elif 'queries' in data:
        queries = data['queries']
    else:
        return jsonify({"success": False, "error": "Aucune requête fournie"})
    
    if not queries:
        return jsonify({"success": False, "error": "Aucune requête trouvée"})
    
    script_path = SCRIPTS[script_id]
    
    # S'assurer que le dossier output existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Exécuter le script pour chaque requête
    for query in queries:
        try:
            #cmd = f'python {script_path} "{query}" "{OUTPUT_DIR}"'
            cmd = f'python -c "import sys; sys.stdout.reconfigure(encoding=\'utf-8\', errors=\'replace\'); exec(open(\'{script_path}\').read())" "{query}" "{OUTPUT_DIR}"'
            process = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
            
            result = {
                "query": query,
                "success": process.returncode == 0,
                "output": process.stdout,
                "error": process.stderr
            }
            
            results.append(result)
            
        except Exception as e:
            results.append({
                "query": query,
                "success": False,
                "output": "",
                "error": str(e)
            })
    
    # Exécuter le script copy_json_to_output.py automatiquement après la recherche
    try:
        # Chemin par défaut où chercher les fichiers JSON
        source_path = "."  # Répertoire courant
        
        # Si vous avez un chemin spécifique où sont générés vos fichiers JSON, remplacez-le ici
        # source_path = "./your_json_folder"  
        
        cmd = f'python copy_json_to_output.py "{source_path}" "{OUTPUT_DIR}"'
        subprocess.run(cmd, shell=True, check=False)
        
    except Exception as e:
        print(f"Erreur lors de la copie des fichiers JSON: {e}")
    
    return jsonify({
        "success": True,
        "results": results
    })

# Récupérer la liste des fichiers de sortie
@app.route('/api/output', methods=['GET'])
def get_output_files():
    if not os.path.exists(OUTPUT_DIR):
        return jsonify([])
    
    files = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(OUTPUT_DIR, filename)
            file_stat = os.stat(file_path)
            
            files.append({
                "name": filename,
                "size": file_stat.st_size,
                "modified": file_stat.st_mtime
            })
    
    return jsonify(sorted(files, key=lambda x: x["modified"], reverse=True))

# Récupérer le contenu d'un fichier de sortie
@app.route('/api/output/<filename>', methods=['GET'])
def get_output_file(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path) or not filename.endswith('.json'):
        return jsonify({"error": "Fichier non trouvé"}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Télécharger un fichier de sortie
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Créer un fichier inputs.txt vide s'il n'existe pas
    if not os.path.exists("inputs.txt"):
        with open("inputs.txt", "w", encoding="utf-8") as f:
            pass
    
    print(f"🚀 Serveur démarré sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
