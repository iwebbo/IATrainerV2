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
from playwright.sync_api import sync_playwright
import json
import time
import sys
import os

# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("issue : python docget_duck3.py 'votre requête'")
    sys.exit(1)



# 🔹 Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]
MAX_RESULTS = 100  # Nombre de résultats à récupérer

# Création du dossier pour stocker les résultats JSON
OUTPUT_DIR = "json\scraped_data_duckduck_search"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Nom du fichier basé sur la requête (remplace les espaces par des underscores)
json_filename = os.path.join(OUTPUT_DIR, f"{SEARCH_QUERY.replace(' ', '_')}.json")

def scrape_duckduckgo(query, max_results):
    """Effectue une recherche sur DuckDuckGo et récupère plusieurs résultats."""
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "summary": r["body"]
            })

    return results

# """     for res in results:
#         print(f"{res['title']}: {res['href']}") """

# 🔹 Sauvegarde des résultats en JSON
def save_to_json(data, filename=json_filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    #print(f"Données sauvegardées dans {filename}")

if __name__ == "__main__":
    scraped_data = scrape_duckduckgo(SEARCH_QUERY, MAX_RESULTS)
    if scraped_data:
        save_to_json(scraped_data)
        #print(f"{len(scraped_data)} résultats récupérés !")
    else:
        print("Aucun résultat trouvé.")

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    # DUCK_PATH = os.path.join(BASE_DIR, "scraper_duck2.py")

    # print("📄 Scrapping all link founds and Génération du PDF...")
    # os.system(f'python "{DUCK_PATH}"')
    # print("✅ Finish.")