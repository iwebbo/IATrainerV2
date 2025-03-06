"""
Copyright (c) 2025 [A&E Coding]

Permission est accordée, gratuitement, à toute personne obtenant une copie
 de ce logiciel et des fichiers de documentation associés (le "IAtrainer.py"),
 de traiter le Logiciel sans restriction, y compris, sans s'y limiter, les droits
 d'utiliser, de copier, de modifier, de fusionner, de publier, de distribuer, de sous-licencier,
 et/ou de vendre des copies du Logiciel, et de permettre aux personnes à qui
 le Logiciel est fourni de le faire, sous réserve des conditions suivantes :

Le texte ci-dessus et cette autorisation doivent être inclus dans toutes les copies
 ou portions substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPLICITE OU IMPLICITE,
Y COMPRIS MAIS SANS S'Y LIMITER, LES GARANTIES DE QUALITÉ MARCHANDE, D'ADÉQUATION
À UN USAGE PARTICULIER ET D'ABSENCE DE CONTREFAÇON. EN AUCUN CAS LES AUTEURS OU TITULAIRES
DU COPYRIGHT NE POURRONT ÊTRE TENUS RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE RESPONSABILITÉ,
QUE CE SOIT DANS UNE ACTION CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE,
OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES INTERACTIONS AVEC LE LOGICIEL.
"""

from duckduckgo_search import DDGS
import json
import os
import sys

# Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("Issue : python docget_duck2.py 'votre requête'")
    sys.exit(1)

# Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]
MAX_RESULTS = 100  # Nombre de résultats à récupérer

# Création du dossier pour stocker les résultats JSON
OUTPUT_DIR = "json\images_results_duck_llm"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Nom du fichier basé sur la requête (remplace les espaces par des underscores)
json_filename = os.path.join(OUTPUT_DIR, f"{SEARCH_QUERY.replace(' ', '_')}.json")

# Exécution de la recherche d'images
with DDGS() as ddgs:
    images = list(ddgs.images(SEARCH_QUERY, max_results=MAX_RESULTS))

# for img in images:
#     print("{img['title']}: {img['href']}")

# Vérifier si des résultats ont été trouvés
if not images:
    print(f"No results found '{SEARCH_QUERY}'")
    sys.exit(1)

# Structurer les résultats au format JSON
formatted_results = {
    "query": SEARCH_QUERY,
    "results": [{"image_url": img["image"], "title": img["title"], "source": img["url"]} for img in images]
}

# Sauvegarde dans un fichier JSON
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(formatted_results, json_file, ensure_ascii=False, indent=4)

print(f"Data save to : {json_filename}")
