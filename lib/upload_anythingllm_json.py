"""
Copyright (c) 2025 [A&E Coding]

Permission est accordée, gratuitement, à toute personne obtenant une copie
 de ce logiciel et des fichiers de documentation associés (le "IAScrapper.py"),
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

"""

import os
import json
import requests

# 🔧 CONFIGURATION
ANYTHINGLLM_API_URL = "http://localhost:3001/api/v1"
ANYTHINGLLM_API_KEY = "0M6D0DJ-QVDMFQB-KNZMBH3-16F5KXH"
WORKSPACE_NAME = "ollamatest"
JSON_FOLDER = "json"  # Dossier contenant les JSON déjà formatés

print (JSON_FOLDER)

headers = {"Authorization": f"Bearer {ANYTHINGLLM_API_KEY}"}

def get_or_create_workspace():
    """
    Vérifie si un workspace existe déjà sur AnythingLLM. S'il n'existe pas, il est créé.
    """
    response = requests.get(f"{ANYTHINGLLM_API_URL}/workspaces", headers=headers)

    try:
        workspaces = response.json()

        if isinstance(workspaces, list):
            for ws in workspaces:
                if ws.get("name") == WORKSPACE_NAME:
                    print(f"✅ Workspace '{WORKSPACE_NAME}' trouvé (Slug: {ws.get('slug')})")
                    return ws.get("slug")

        print(f"🚀 Création du workspace '{WORKSPACE_NAME}'...")
        create_response = requests.post(
            f"{ANYTHINGLLM_API_URL}/workspace/new",
            json={"name": WORKSPACE_NAME},
            headers=headers,
        )

        if create_response.status_code == 200:
            workspace_data = create_response.json()
            print(f"✅ Workspace '{WORKSPACE_NAME}' créé (Slug: {workspace_data.get('slug')})")
            return workspace_data.get("slug")

        else:
            print(f"❌ Erreur lors de la création du workspace : {create_response.text}")
            return None

    except requests.exceptions.JSONDecodeError:
        print(f"❌ Erreur : la réponse n'est pas en JSON !\nRéponse brute : {response.text}")
        return None

def upload_json_to_anythingllm(workspace_slug):
    """
    Envoie directement chaque fichier JSON à AnythingLLM.
    """
    uploaded_files = 0

    for filename in os.listdir(JSON_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(JSON_FOLDER, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                json_data = json.load(file)  # Charge le JSON tel quel, sans modification

            # Construire la requête d'upload
            upload_url = f"{ANYTHINGLLM_API_URL}/workspace/{workspace_slug}/update"
            payload = {"name": filename, "content": json.dumps(json_data)}  # Envoie tel quel

            response = requests.post(upload_url, json=payload, headers=headers)

            if response.status_code == 200:
                print(f"✅ {filename} uploadé avec succès !")
                uploaded_files += 1
            else:
                print(f"❌ Échec de l'upload de {filename} : {response.text}")

    return uploaded_files

# 🚀 Exécution du script
if __name__ == "__main__":
    ws_slug = get_or_create_workspace()
    if ws_slug:
        total_uploaded = upload_json_to_anythingllm(ws_slug)
        print(f"\n🎯 {total_uploaded} fichiers JSON envoyés à AnythingLLM !")

