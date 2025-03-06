"""
Copyright (c) 2025 [A&E Coding]

Permission est accordée, gratuitement, à toute personne obtenant une copie
 de ce logiciel et des fichiers de documentation associés (le "IAtrainer.py"),
 de traiter le Logiciel sans restriction, y compris, sans s'y limiter, les droits
 d'utiliser, de copier, de modifier, de fusionner, de publier, de distribuer, de sous-licencier,
 et/ou de vendre des copies du Logiciel, et de permettre aux personnes à qui
 le Logiciel est fourni de le faire, sous réserve des conditions suivantes :

"""

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from duckduckgo_search import DDGS
import json
import os
import sys

# Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("Issue : python docget_duck2.py 'request'")
    sys.exit(1)

# Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]
MAX_RESULTS = 100  # Nombre de résultats à récupérer

# Création du dossier pour stocker les résultats JSON
OUTPUT_DIR = "json\ews_results_duck_llm"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Nom du fichier basé sur la requête (remplace les espaces par des underscores)
json_filename = os.path.join(OUTPUT_DIR, f"{SEARCH_QUERY.replace(' ', '_')}.json")

with DDGS() as ddgs:
    results = ddgs.news(SEARCH_QUERY, max_results=MAX_RESULTS)

structured_results = [
    {
        "title": result["title"],
        "url": result["url"],      # Utilise "url" et non "href"
        "snippet": result["body"],
        "date": result["date"],
        "source": result["source"]
    }
    for result in results
]

with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(structured_results, json_file, ensure_ascii=False, indent=4)

print("Save data json \eews_results_duck_llm.json")