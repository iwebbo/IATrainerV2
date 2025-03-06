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

import json
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import time
from playwright.sync_api import sync_playwright
import sys
import os



# 🔹 Récupération du BASE_DIR depuis `main.py`
BASE_DIR = sys.argv[2] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

# 🔹 Correction des chemins relatifs en utilisant BASE_DIR
FONT_PATH = os.path.join(BASE_DIR, "pdf", "DejaVuSans.ttf")  # Police TTF
PDF_DIR = os.path.join(BASE_DIR, "pdf")  # Dossier PDF
JSON_FILE = os.path.join(BASE_DIR, "scrap", "scrapped_menu_links_doc.json")  # JSON
PDF_FILE = "Documentation_Site.pdf"


def scrape_page(url):
    """Scrape le contenu principal d'une page Ansible en exécutant le JavaScript."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Attendre que le contenu principal se charge
        page.wait_for_selector("div.document", timeout=20000)

        # Récupérer le HTML après rendu
        html_content = page.content()
        browser.close()

    soup = BeautifulSoup(html_content, "html.parser")

    # Extraire le bon élément contenant le texte
    content = soup.select_one("div.document")
    if not content:
        print(f"Issue with {url}")
        return ""

    return content.get_text(separator="\n", strip=True)

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", size=16)
        self.cell(200, 10, "Documentation Ansible", ln=True, align="C")
        self.ln(10)

def save_to_pdf(content_list, output_file=PDF_FILE):
    """Sauvegarde le contenu dans un PDF en UTF-8."""
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Ajouter la police UTF-8
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)

    for title, text in content_list:
        pdf.add_page()
        pdf.set_font("DejaVu", size=14)
        pdf.cell(200, 10, title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 10, text)

    pdf.output(output_file)
    print(f"Save to PDF : {output_file}")

def main():
    """Exécute le scraping et la création du PDF."""
    print("📖 Lecture du fichier JSON contenant les liens...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        links = json.load(f)

    if not links:
        print("Issue stopping script.")
        return

    content_list = []

    for entry in links:
        title, url = entry["title"], entry["url"]
        print(f"📄 Scraping : {title}")
        text = scrape_page(url)
        if text:
            content_list.append((title, text))
        time.sleep(1)  # Évite le bannissement

    print("📄 Génération du PDF...")
    save_to_pdf(content_list)

if __name__ == "__main__":
    main()
