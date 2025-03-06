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

"""
README:

pip install beautifulsoup4 requests playwright
playwright install

"""
from playwright.sync_api import sync_playwright
import json
import sys
import os

# 🔹 Vérifier si un argument est fourni
if len(sys.argv) < 2:
    print("❌ Erreur : Aucun terme de recherche fourni. Exécution : python docget_stackflow.py 'votre requête'")
    sys.exit(1)

# 🔹 Récupérer la requête depuis l'argument
SEARCH_QUERY = sys.argv[1]

# 🔹 Configuration
BASE_URL = "https://stackoverflow.com/search?q="
JSON_FILE = "json\scraped_data_stackflow.json"

def scrape_with_playwright(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 🔹 Mettre headless=True si pas besoin de voir
        page = browser.new_page()
        page.goto(f"{BASE_URL}{query.replace(' ', '+')}", timeout=60000)

        # 🔹 Attendre que le CAPTCHA soit résolu manuellement
        input("⚠️ Résolvez le CAPTCHA, puis appuyez sur Entrée...")

        # 🔹 Scraper les résultats
        posts = page.query_selector_all("div.s-post-summary")
        for post in posts:
            title = post.query_selector("a.s-link").inner_text()
            link = "https://stackoverflow.com" + post.query_selector("a.s-link").get_attribute("href")
            summary = post.query_selector("div.s-post-summary--content-excerpt").inner_text() if post.query_selector("div.s-post-summary--content-excerpt") else ""
            results.append({"title": title, "link": link, "summary": summary})

        browser.close()

    return results

# 🔹 Sauvegarde en JSONL
def save_to_json(data, filename=JSON_FILE):
    """Sauvegarde les données en JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # ✅ Écriture en JSON formaté
    print(f"✅ Données sauvegardées dans {filename}")


if __name__ == "__main__":
    scraped_data = scrape_with_playwright(SEARCH_QUERY)
    if scraped_data:
        save_to_json(scraped_data)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    STACK_PATH = os.path.join(BASE_DIR, "scraper_stack.py")

    # print("📄 Scrapping all link founds and Génération du PDF...")
    # os.system(f'python "{STACK_PATH}"')
    # print("✅ Finish.")
